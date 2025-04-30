RESERVED_POINTS_FOR_MANDATORY_KEYWORDS = 60
RESERVED_POINTS_FOR_OPTIONAL_KEYWORDS = 40

ROLE_MATCHING_DEFINITIONS = {
    "REACT_DEVELOPER": {
        "mandatory": ["React", "JavaScript", "HTML", "CSS", "Redux", "Git"],
        "optional_groups": [
            {
                "name": "Redux Ecosystem",
                "weight": 10,
                "terms": [
                    "Thunk",
                    "Saga",
                    "RTK",
                    "Redux Toolkit",
                ],
            },
            {
                "name": "Testing",
                "weight": 8,
                "terms": [
                    "Jest",
                    "Mocha",
                    "Enzyme",
                    "Cypress",
                ],
            },
            {
                "name": "Build Tools",
                "weight": 5,
                "terms": ["Webpack", "Vite", "Rollup", "Parcel", "Babel", "Esbuild"],
            },
            {
                "name": "DevOps & Deployment",
                "weight": 5,
                "terms": [
                    "AWS",
                    "Docker",
                    "Kubernetes",
                    "CI/CD",
                    "Terraform",
                    "GCP",
                    "Azure",
                    "Google Cloud",
                    "S3",
                    "EC2",
                ],
            },
            {
                "name": "JS Backend Frameworks",
                "weight": 5,
                "terms": [
                    "NodeJS",
                    "Expressjs",
                    "NextJS",
                ],
            },
            {
                "name": "Python Backend Frameworks",
                "weight": 7,
                "terms": ["Python", "Django", "FastAPI"],
            },
            {
                "name": "Database",
                "weight": 5,
                "terms": ["MySQL", "PostgreSQL", "MongoDB", "Mongo", "SQL", "NoSQL"],
            },
            {
                "name": "Project Management",
                "weight": 3,
                "terms": ["Agile", "Scrum", "Jira"],
            },
            {
                "name": "Performance Optimization",
                "weight": 7,
                "terms": [
                    "Code splitting",
                    "Lazy loading",
                    "Web vitals",
                    "Performance optimization",
                ],
            },
        ],
    },
    "JAVA_DEVELOPER": {
        "mandatory": ["Java", "Spring", "SQL", "Git"],
        "optional_groups": [
            {
                "name": "Java Ecosystem",
                "weight": 10,
                "terms": [
                    "JSP",
                    "Servlets",
                    "Spring Boot",
                    "Hibernate",
                    "JPA",
                    "JDBC",
                    "Multithreading",
                    "Synchronization",
                    "Maven",
                    "Gradle",
                    "JUnit",
                    "Mockito",
                    "Java 8+",
                    "Microservices",
                ],
            },
            {
                "name": "Web Services & Protocols",
                "weight": 9,
                "terms": [
                    "REST",
                    "SOAP",
                    "OpenSPML",
                    "API",
                    "Web Services",
                    "HTTP",
                    "XML",
                    "JSON",
                ],
            },
            {
                "name": "Frontend & UI",
                "weight": 7,
                "terms": [
                    "HTML",
                    "CSS",
                    "JavaScript",
                    "jQuery",
                    "TypeScript",
                    "Angular",
                    "React",
                ],
            },
            {
                "name": "Architecture Patterns",
                "weight": 8,
                "terms": [
                    "MVC",
                    "Architectural Patterns",
                    "Design Patterns",
                    "DDD",
                    "CQRS",
                    "Clean Architecture",
                    "Hexagonal Architecture",
                    "Code Review",
                ],
            },
            {
                "name": "Database Technologies",
                "weight": 8,
                "terms": [
                    "SQL",
                    "JDBC",
                    "ORM",
                    "Oracle",
                    "PostgreSQL",
                    "MySQL",
                    "MongoDB",
                    "NoSQL",
                ],
            },
            {
                "name": "DevOps & Version Control",
                "weight": 8,
                "terms": [
                    "CI/CD",
                    "Git",
                    "SVN",
                    "Branching",
                    "Merging",
                    "Docker",
                    "Jenkins",
                    "Continuous Integration",
                    "Continuous Deployment",
                ],
            },
            {
                "name": "Performance & Quality",
                "weight": 6,
                "terms": [
                    "Code Quality",
                    "Code Reviews",
                    "JVM Tuning",
                    "Profiling",
                    "Testing",
                    "Performance Optimization",
                ],
            },
            {
                "name": "Cloud & DevOps",
                "weight": 5,
                "terms": [
                    "AWS",
                    "Docker",
                    "Kubernetes",
                    "Jenkins",
                    "Azure",
                    "GCP",
                    "Cloud Native",
                ],
            },
            {
                "name": "Security",
                "weight": 4,
                "terms": [
                    "OAuth",
                    "JWT",
                    "Spring Security",
                    "Authentication",
                    "Authorization",
                ],
            },
        ],
    },
}

JOB_DESC_FOR_REACT_DEVELOPER = """
Job Description

React JS Developer

Experience: 1-3 Years

We are looking for a rockstar JavaScript developer who is proficient with Javascript Frameworks. Your primary focus will be on developing user interface components and implementing them following well-known React.js workflows (such as Flux or Redux). You will ensure that these components and the overall application are robust and easy to maintain. You will coordinate with the rest of the team working on different layers of the infrastructure. Therefore, a commitment to collaborative problem solving, sophisticated design, and quality products are important.

Technical Skills:
● Proficient in any of these frameworks: Backbone JS, VueJS, AngularJS, React Js
● We work with React+Redux so knowledge of these will be plus
● Experience working with modern Javascript libraries and tools like ES6/ES7, and Webpack
● Experience with unit testing in any modern javascript library (Jest/Mocha/Jasmine)
● Keeps an eye on new front-end ecosystem changes
● Knowledge of TypeScript and node js (Relay+Graph ql) would be a plus
● Proficient in HTML & CSS
● Sense for appeal & aesthetics from a usability perspective

Soft Skills:
● Obsessed with best practices and have an eye for detail
● Self-starter with a high level of drive and commitment
● High energy and drive to work in a startup environment
● Conceptual thinking, flexibility, and ability to juggle multiple responsibilities
● Ability to work under pressure and confidence to deal with complex issues
● Strong communication skills
● Hands-on and detail-oriented
"""


JOB_DESC_FOR_JAVA_DEVELOPER = """
Role: Senior Software Engineer (Java)
Location: Thane
Experience: 4+ years

Role & Responsibilities:
- Strong proficiency in Java with a solid understanding of its ecosystem.
- Good knowledge of Object-Oriented Programming (OOP) concepts and design patterns.
- Design and implement functional modules using various architectural patterns.
- Ensure implementation follows the MVC (Model-View-Controller) pattern.
- Use version control tools (GIT) for merging, branching, and version management.
- Conduct code reviews to maintain high code quality.
- Write complex/medium SQL queries efficiently.
- Expertise in Continuous Integration and Deployment (CI/CD).

Technical Skills Required:
- Java Server Pages (JSP) & Servlets
- Spring Framework (Spring Boot preferred)
- Hibernate (ORM Framework)
- JDBC (Java Database Connectivity)
- REST Web Services, Open SPML
- SQL (Basic knowledge is mandatory)
- HTML, JavaScript, CSS, and jQuery
- Understanding of XML & JSON
- Multithreading and synchronization concepts
"""

__MOCK_LLM_MODE__ = True
