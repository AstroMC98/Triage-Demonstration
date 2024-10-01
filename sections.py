hero_section = """
<section id="templates" class="templates section">
    <div class="row align-items-xl-center gy-5">
        <div class="col-xl-5 content">
            <h3>
                SmartPulse Triage Platform
            </h3>
            <h2>
                Transform Your Prioritization Systems with SmartPulse
            </h2>
            <p>
                SmartPulse is an innovative platform designed to revolutionize how businesses across industries manage and prioritize incoming requests. Whether you're running a busy clinic, handling a flood of IT support tickets, or organizing internal business workflows, SmartPulse delivers a smart, adaptable solution for ensuring critical tasks are handled with the right level of urgency. By using intelligent, data-driven insights, SmartPulse empowers your team to make faster, more informed decisions—ultimately reducing delays, improving response times, and enhancing customer satisfaction. No matter the industry, SmartPulse seamlessly integrates into your existing processes, offering flexibility and precision that drives productivity and better outcomes.
            </p>
            <a href="#" class="read-more">
                <span>
                    Try the Demo
                </span>
            </a>
        </div>
        <div class="col-xl-7">
            <div class="section-guide">
                <h4>
                    Simplify and Streamline Your Workflow with SmartPulse
                </h4>
                <p>
                    <strong>Assign:</strong> From the moment a request comes in—be it a patient inquiry, an IT support ticket, or an important business task—SmartPulse enables you to effortlessly log critical information into the platform. The intuitive webapp allows your team to capture essential details with speed and accuracy, ensuring nothing slips through the cracks. For healthcare providers, this means gathering key patient information right from the initial call, while in IT, it could be a support technician instantly categorizing and assigning the appropriate ticket. In business environments, SmartPulse helps executives prioritize projects or emails, ensuring that high-impact tasks receive the attention they deserve.
                </p>
                <p>
                    <strong>Review:</strong> Once requests are logged, SmartPulse generates tailored resolutions based on predefined criteria and AI-driven insights. Whether you're in healthcare, IT, or business management, the platform quickly sorts and prioritizes each entry according to urgency and relevance. For IT teams, this could mean automatically highlighting critical server outages, while business professionals might see high-priority client emails or projects moved to the top of their queue. In each case, the AI ensures your team focuses on what matters most. By offering a bird's-eye view of all tasks or cases, SmartPulse allows for easy review and adjustment, empowering decision-makers to stay ahead of potential issues and streamline workflow.
                </p>
            </div>
        </div>
    </div>
</section>
<hr class="hr hr-blurry"/>
<div class="container section-title">
    <h2>
        SmartPulse Triage
    </h2>
    <p>
        Leverage on AI to simplify, accelerate, and enhance your triage systems.
    </p>
</div>
"""

hero_css = """
<style>

    .st-emotion-cache-gi0tri{
        display : none;
    }

    .section {
        padding-top : 60px;
        padding-bottom : 30px;
        scroll-margin-top: 98px;
        overflow: clip;
    }
    
    .align-item-xl-center {
        align-items: center !important;
    }
    
    .g-5, .gy-5 {
        --bs-gutter-y : 3rem;
    }
    
    .g-4, .gy-4 {
        --bs-gutter-y : 3rem;
    }
    
    .row {
        --bs-gutter-x : 1.5rem;
        --bs-gutter-y : 0;
        display : flex;
        flex-wrap : wrap;
        margin-top : -3rem;
        margin-right : 0rem;
        margin-left : 0rem;
    }
    
    .col-xl-5 {
        flex : 0 0 auto;
        width: 41.6667%;
        justify-content: center;
        padding-top : 4rem;
        padding-bottom: 0rem;
    }
    
    .col-xl-7 {
        flex: 0 0 auto;
        width: 58.333%;
    }
    
    .templates .content h3 {
        font-size : 16px;
        font-weight : 500;
        line-height : 19px;
        padding : 10px 20px;
        border-radius : 7px;
        display : inline-block;
        background : color-mix(in srgb, #2197bd, transparent 95%);
        color : #2197bd;
        
        margin-top : 1rem;
        margin-bottom : 0rem;
        margin-block-start : 1em;
        margin-block-end : 1em;
        margin-inline-start : 0px;
        margin-inline-end : 0px;
        --bs-gutter-y : 3rem;
        --bs-gutter-x : 1.5rem;
    }
    
    .templates .content h2 {
        font-size : 2rem;
        font-weight : 700;
        line-height : 1.2;
        
        margin-top : 0;
        margin-bottom : .5rem;
        margin-inline-start : 0px;
        margin-inline-end : 0px;
        
        padding-top : 0;
        padding-bottom : 0;
    }
    
    .templates .content p {
        display: block;
        
        margin-top : 0;
        margin-bottom : 1rem;
        margin-block-start : 1em;
        margin-block-end : 1em;
        margin-inline-start : 0px;
        margin-inline-end : 0px;
        
        unicode-bidi: isolate;
    }
    
    .templates .content .read-more {
        background : #2197bd;
        color : #fff;
        font-family : "Montserrat", sans-serif;
        font-weight : 500;
        font-size : 16px;
        letter-spacing : 1px;
        padding : 12px 24px;
        border-radius : 5px;
        transition : 0.3s;
        display : inline-flex;
        align-items : center;
        justify-content : center;
        text-decoration : none;
    }
    
    .templates .content .read-more:hover {
        background : color-mix(in srgb, #2197bd, transparent 20%);
        padding-right: 25px;
    }
    
    .col-xl-7 .section-guide {
        background-color : #fff;
        padding: 50px 40px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
        border-radius: 10px;
        margin : 20px;
        transition : all 0.3s ease
    }
    
    .section-title {
        text-align : center;
        padding-bottom : 5px;
        position : relative;
    }
    
    .container {
        --bs-gutter-x : 1.5rem;
        --bs-gutter-y : 0;
        width : 100%;
        padding-right: calc(var(--bs-gutter-x)* .5);
        padding-left: calc(var(--bs-gutter-x)* .5);
        margin-right: auto;
        margin-left: auto;
    }
    
    .section-title h2 {
        font-size: 32px;
        font-weight: 700;
        position: relative;
        line-height: 1.2;
        margin-top: 0;
        margin-bottom: .5rem;
        margin-block-start: 0.83em;
        margin-block-end: 0em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        padding-bottom : 5px;
    }
    
    .section-title h2:before {
        margin: 0 15px 10px 0;
    }
    
    .section-title h2:after {
        margin: 0 0 10px 15px;
    }
    
    .section-title h2:before, .section-title h2:after {
        content: "";
        width: 50px;
        height: 2px;
        background: #2197bd;
        display: inline-block;
    }
    
    .section-title p{
        margin-top: 1.5rem;
        margin-bottom: 0;
        display: block;
        margin-block-start: 0em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        text-align: center;
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.5;
    }
    
    .hr-blurry {
        border: none;
        height: 2px;
        background: rgba(0,0,0,0.1);
        backdrop-filter: blur(5px);
        margin: 20px 0;
        opacity: 0.7;
    }
    
    .hr-blurry-templates {
        border: none;
        height: 2px;
        background: #2197bd;
        backdrop-filter: blur(5px);
        margin-top: -5px;
        margin-right: 0px;
        margin-bottom: 10px;
        margin-left: 0px
        opacity: 0.4;
    }
    
</style>
"""

triage_generate_results="""
<div class="row-generate">
    <div class="col-6 d-flex align-items-start">
        <section id="about" class="customize-section">
            <div class="customize-container customize-section-title aos-init aos-animate" data-aos="fade-up">
                <h2>Patient</h2>
                <p>Triage Request</p>
            </div>
        </section>
    </div>
    <div class="col-6 d-flex justify-content-end">
        <div class="invoice-from">
            <ul class="list-unstyled text-right">
                <li>SMX Convention Center</li>
                <li>Echelon Portfolio Showcase</li>
            </ul>
        </div>
    </div>
</div>
<div class="col-12">
    <div class="invoice-details mt25">
        <div class="well">
            <ul class="list-unstyled mb0">
                <li><strong>Reference ID</strong> #{referenceID}</li>
                <li><strong>Request Date:</strong> {dateOfrequest}</li>
                <li><strong>Patient Name:</strong> {patientName}</li>
                <li><strong>Age Bracket:</strong> {ageBracket}</li>
                <li><strong>Contact Number:</strong> {contactNumber}</li>
                <li><strong>Patient Concern:</strong> {condition}</li>
                <li><strong>Additional Information:</strong> {addtlInfo}</li>
                <li><strong>Triage Status:</strong> <span class="label label-danger">FOR SCHEDULING</span></li>
            </ul>
        </div>
    </div>
</div>
"""

triage_review_section_header = """
<div class="row-generate">
    <div class="col-6 d-flex align-items-start">
        <section id="about" class="customize-section">
            <div class="customize-container customize-section-title aos-init aos-animate" data-aos="fade-up">
                <h2>Patient</h2>
                <p>Triage Database</p>
            </div>
        </section>
    </div>
    <div class="col-6 d-flex justify-content-end">
        <div class="invoice-from">
            <ul class="list-unstyled text-right">
                <li>Demo Database</li>
            </ul>
        </div>
    </div>
</div>
"""

triage_scheduled_results="""
<div class="row-generate">
    <div class="col-6 d-flex align-items-start">
        <section id="about" class="customize-section">
            <div class="customize-container customize-section-title aos-init aos-animate" data-aos="fade-up">
                <h2>Patient</h2>
                <p>Triage Request</p>
            </div>
        </section>
    </div>
    <div class="col-6 d-flex justify-content-end">
        <div class="invoice-from">
            <ul class="list-unstyled text-right">
                <li>SMX Convention Center</li>
                <li>Echelon Portfolio Showcase</li>
            </ul>
        </div>
    </div>
</div>
<div class="col-12">
    <div class="invoice-details mt25">
        <div class="well">
            <ul class="list-unstyled mb0">
                <li><strong>Reference ID</strong> #{referenceID}</li>
                <li><strong>Request Date:</strong> {dateOfrequest}</li>
                <li><strong>Patient Name:</strong> {patientName}</li>
                <li><strong>Age Bracket:</strong> {ageBracket}</li>
                <li><strong>Contact Number:</strong> {contactNumber}</li>
                <li><strong>Patient Concern:</strong> {condition}</li>
                <li><strong>Additional Information:</strong> {addtlInfo}</li>
                <li><strong>Triage Status:</strong> <span class="label label-success">SCHEDULED</span></li>
                <li><strong>Triage Assignment:</strong> {triage}</li>
                <li><strong>Triage Notes:</strong> {triageNotes}</li>
            </ul>
        </div>
    </div>
</div>
"""