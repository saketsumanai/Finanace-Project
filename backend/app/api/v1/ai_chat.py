"""
AI Chat API endpoints using Google Gemini with Alpha Vantage integration.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.project import Project
from app.models.production_data import ProductionData
from app.models.financial_data import FinancialData
from app.api.deps import get_current_user
from app.services.gemini_service import get_gemini_service


router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    project_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    suggestions: Optional[List[str]] = None


class ProjectAnalysisRequest(BaseModel):
    """Project analysis request."""
    project_id: int


class OptimizeAssumptionsRequest(BaseModel):
    """Optimize assumptions request."""
    project_id: int


class AnalyzeResultsRequest(BaseModel):
    """Analyze results request."""
    scenario_id: int


class SuggestSynergiesRequest(BaseModel):
    """Suggest synergies request."""
    project_id: int
    assumptions_id: Optional[int] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    data: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI about projects and valuations with real-time market data.
    
    Args:
        data: Chat message
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        AI response with market intelligence
    """
    try:
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        
        # Get project context if project_id provided
        project_context = {}
        if data.project_id:
            project = db.query(Project).filter(
                Project.id == data.project_id,
                Project.owner_id == current_user.id
            ).first()
            
            if project:
                project_context = {
                    'name': project.name,
                    'project_type': project.project_type,
                    'deal_size': float(project.deal_size) if project.deal_size else 0,
                    'description': project.description
                }
        
        # Check if user wants market data analysis
        message_lower = data.message.lower()
        wants_market_data = any(keyword in message_lower for keyword in [
            'market', 'price', 'oil', 'gas', 'commodity', 'current', 'today', 'now'
        ])
        
        # Get AI response with optional market data
        if wants_market_data and gemini.alpha_vantage:
            response = gemini.analyze_with_market_data(
                data.message,
                include_commodities=True
            )
        elif project_context:
            response = gemini.chat_about_project(data.message, project_context)
        else:
            response = gemini.send_message(data.message)
        
        # Generate suggestions based on message
        suggestions = []
        if 'assumption' in data.message.lower():
            suggestions = [
                "What decline rate should I use?",
                "How do I calculate discount rate?",
                "What's a typical exit multiple?"
            ]
        elif 'synerg' in data.message.lower():
            suggestions = [
                "What synergies should I consider?",
                "How do I estimate cost synergies?",
                "What's a realistic realization timeline?"
            ]
        elif 'risk' in data.message.lower():
            suggestions = [
                "What are the key risks?",
                "How do I mitigate production risk?",
                "What about commodity price risk?"
            ]
        elif wants_market_data:
            suggestions = [
                "What's the market outlook for oil & gas?",
                "How do current prices affect valuation?",
                "Should I hedge commodity prices?"
            ]
        
        return ChatResponse(
            response=response,
            suggestions=suggestions if suggestions else None
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI chat error: {str(e)}"
        )


@router.post("/analyze-project")
async def analyze_project(
    data: ProjectAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI analysis of a project.
    
    Args:
        data: Project analysis request
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        AI analysis with insights
    """
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == data.project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Prepare project data
        project_data = {
            'name': project.name,
            'project_type': project.project_type,
            'deal_size': float(project.deal_size) if project.deal_size else 0,
            'description': project.description
        }
        
        # Get AI analysis
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        analysis = gemini.analyze_project(project_data)
        
        return {
            'success': True,
            'project_id': data.project_id,
            'analysis': analysis
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis error: {str(e)}"
        )


@router.post("/optimize-assumptions")
async def optimize_assumptions(
    data: OptimizeAssumptionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-optimized assumptions based on project data.
    
    Args:
        data: Optimize assumptions request
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Optimized assumptions
    """
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == data.project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Get historical data summary
        production_data = db.query(ProductionData).filter(
            ProductionData.project_id == data.project_id
        ).all()
        
        financial_data = db.query(FinancialData).filter(
            FinancialData.project_id == data.project_id
        ).all()
        
        avg_oil = sum(float(p.oil_volume or 0) for p in production_data) / len(production_data) if production_data else 0
        avg_gas = sum(float(p.gas_volume or 0) for p in production_data) / len(production_data) if production_data else 0
        
        project_data = {
            'project_type': project.project_type,
            'deal_size': float(project.deal_size) if project.deal_size else 0
        }
        
        historical_data = {
            'production_count': len(production_data),
            'financial_count': len(financial_data),
            'avg_oil': avg_oil,
            'avg_gas': avg_gas
        }
        
        # Get AI recommendations
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        recommendations = gemini.optimize_assumptions(project_data, historical_data)
        
        return {
            'success': True,
            'project_id': data.project_id,
            'recommendations': recommendations
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Optimization error: {str(e)}"
        )


@router.post("/analyze-results")
async def analyze_results(
    data: AnalyzeResultsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI analysis of valuation results.
    
    Args:
        data: Analyze results request
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        AI analysis and recommendation
    """
    try:
        from app.models.scenario import Scenario
        from app.engines.valuation_service import ValuationService
        
        # Get scenario
        scenario = db.query(Scenario).filter(
            Scenario.id == data.scenario_id
        ).first()
        
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )
        
        # Verify user has access
        project = db.query(Project).filter(
            Project.id == scenario.project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get valuation results
        valuation_service = ValuationService(db)
        results = valuation_service.get_valuation_results(str(data.scenario_id))
        
        # Get AI analysis
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        analysis = gemini.analyze_valuation_results(results)
        
        return {
            'success': True,
            'scenario_id': data.scenario_id,
            'analysis': analysis
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis error: {str(e)}"
        )


@router.post("/suggest-synergies")
async def suggest_synergies(
    data: SuggestSynergiesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-suggested synergies for a project.
    
    Args:
        data: Suggest synergies request
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Suggested synergies
    """
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == data.project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        project_data = {
            'project_type': project.project_type,
            'deal_size': float(project.deal_size) if project.deal_size else 0
        }
        
        assumptions = {}
        if data.assumptions_id:
            from app.models.assumptions import Assumptions
            assumptions_obj = db.query(Assumptions).filter(
                Assumptions.id == data.assumptions_id
            ).first()
            if assumptions_obj:
                assumptions = {
                    'decline_rate': float(assumptions_obj.decline_rate),
                    'discount_rate': float(assumptions_obj.discount_rate)
                }
        
        # Get AI suggestions
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        suggestions = gemini.suggest_synergies(project_data, assumptions)
        
        return {
            'success': True,
            'project_id': data.project_id,
            'synergies': suggestions
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Suggestion error: {str(e)}"
        )


@router.post("/generate-report")
async def generate_report(
    data: AnalyzeResultsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered executive summary report.
    
    Args:
        data: Analyze results request
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Executive summary
    """
    try:
        from app.models.scenario import Scenario
        from app.engines.valuation_service import ValuationService
        
        # Get scenario
        scenario = db.query(Scenario).filter(
            Scenario.id == data.scenario_id
        ).first()
        
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )
        
        # Get project
        project = db.query(Project).filter(
            Project.id == scenario.project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        project_data = {
            'name': project.name,
            'project_type': project.project_type,
            'deal_size': float(project.deal_size) if project.deal_size else 0
        }
        
        # Get valuation results
        valuation_service = ValuationService(db)
        results = valuation_service.get_valuation_results(str(data.scenario_id))
        
        # Generate report
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        summary = gemini.generate_report_summary(project_data, results)
        
        return {
            'success': True,
            'scenario_id': data.scenario_id,
            'executive_summary': summary
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation error: {str(e)}"
        )


@router.post("/analyze-csv")
async def analyze_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze uploaded CSV file with AI.
    
    Args:
        file: Uploaded CSV file
        current_user: Current authenticated user
    
    Returns:
        AI analysis of the CSV data
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only CSV files are supported"
            )
        
        # Read file content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Get AI analysis
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        analysis = gemini.analyze_csv_data(csv_content, file.filename)
        
        return analysis
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CSV analysis error: {str(e)}"
        )


@router.post("/market-intelligence")
async def get_market_intelligence(
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive market intelligence with real-time data.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Market intelligence report
    """
    try:
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        
        if not gemini.alpha_vantage:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Alpha Vantage integration not available"
            )
        
        intelligence = gemini.get_market_intelligence()
        
        return {
            'success': True,
            'report': intelligence,
            'timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Market intelligence error: {str(e)}"
        )


class ComparableCompaniesRequest(BaseModel):
    """Comparable companies analysis request."""
    symbols: List[str]


@router.post("/comparable-companies")
async def analyze_comparable_companies(
    data: ComparableCompaniesRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze comparable oil & gas companies.
    
    Args:
        data: List of company symbols
        current_user: Current authenticated user
    
    Returns:
        Comparable company analysis
    """
    try:
        if not data.symbols or len(data.symbols) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one company symbol required"
            )
        
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        
        if not gemini.alpha_vantage:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Alpha Vantage integration not available"
            )
        
        analysis = gemini.analyze_comparable_companies(data.symbols)
        
        return {
            'success': True,
            'symbols': data.symbols,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparable companies analysis error: {str(e)}"
        )


class AnalyzeAnythingRequest(BaseModel):
    """Analyze anything request."""
    content: str
    content_type: str = "auto"


@router.post("/analyze-anything")
async def analyze_anything(
    data: AnalyzeAnythingRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Advanced AI that can analyze ANYTHING.
    
    Args:
        data: Content to analyze
        current_user: Current authenticated user
    
    Returns:
        Comprehensive analysis
    """
    try:
        if not data.content or len(data.content.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content is required"
            )
        
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        analysis = gemini.analyze_anything(data.content, data.content_type)
        
        return {
            'success': True,
            'content_type': data.content_type,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis error: {str(e)}"
        )


class ScrapeURLRequest(BaseModel):
    """Scrape URL request."""
    url: str
    analysis_focus: str = "general"


@router.post("/scrape-url")
async def scrape_and_analyze_url(
    data: ScrapeURLRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Scrape a URL and get AI analysis.
    
    Args:
        data: URL and analysis focus
        current_user: Current authenticated user
    
    Returns:
        Scraped content with AI analysis
    """
    try:
        if not data.url or not data.url.startswith(('http://', 'https://')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid URL is required (must start with http:// or https://)"
            )
        
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        
        if not gemini.web_scraper:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Web scraping service not available"
            )
        
        analysis = gemini.scrape_and_analyze_url(data.url, data.analysis_focus)
        
        return {
            'success': True,
            'url': data.url,
            'analysis_focus': data.analysis_focus,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Web scraping error: {str(e)}"
        )


class ScrapeMultipleURLsRequest(BaseModel):
    """Scrape multiple URLs request."""
    urls: List[str]


@router.post("/scrape-multiple-urls")
async def scrape_and_compare_urls(
    data: ScrapeMultipleURLsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Scrape multiple URLs and get comparative analysis.
    
    Args:
        data: List of URLs
        current_user: Current authenticated user
    
    Returns:
        Comparative analysis of all URLs
    """
    try:
        if not data.urls or len(data.urls) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one URL is required"
            )
        
        if len(data.urls) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 5 URLs allowed"
            )
        
        # Validate URLs
        for url in data.urls:
            if not url.startswith(('http://', 'https://')):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid URL: {url}"
                )
        
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        
        if not gemini.web_scraper:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Web scraping service not available"
            )
        
        analysis = gemini.scrape_multiple_urls_and_compare(data.urls)
        
        return {
            'success': True,
            'urls': data.urls,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multi-URL scraping error: {str(e)}"
        )


class ResearchTopicRequest(BaseModel):
    """Research topic request."""
    topic: str
    num_sources: int = 5


@router.post("/research-topic")
async def research_topic(
    data: ResearchTopicRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Research a topic by searching and analyzing multiple sources.
    
    Args:
        data: Topic and number of sources
        current_user: Current authenticated user
    
    Returns:
        Comprehensive research report
    """
    try:
        if not data.topic or len(data.topic.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Topic is required"
            )
        
        if data.num_sources < 1 or data.num_sources > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of sources must be between 1 and 10"
            )
        
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        
        if not gemini.web_scraper:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Web scraping service not available"
            )
        
        report = gemini.research_topic(data.topic, data.num_sources)
        
        return {
            'success': True,
            'topic': data.topic,
            'num_sources': data.num_sources,
            'report': report,
            'timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Research error: {str(e)}"
        )


class AnalyzeCompanyWebsiteRequest(BaseModel):
    """Analyze company website request."""
    url: str


@router.post("/analyze-company-website")
async def analyze_company_website(
    data: AnalyzeCompanyWebsiteRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a company website for M&A intelligence.
    
    Args:
        data: Company website URL
        current_user: Current authenticated user
    
    Returns:
        Company analysis
    """
    try:
        if not data.url or not data.url.startswith(('http://', 'https://')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid URL is required"
            )
        
        gemini = get_gemini_service(settings.GEMINI_API_KEY, settings.ALPHA_VANTAGE_API_KEY)
        
        if not gemini.web_scraper:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Web scraping service not available"
            )
        
        analysis = gemini.analyze_company_website(data.url)
        
        return {
            'success': True,
            'url': data.url,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Company website analysis error: {str(e)}"
        )
