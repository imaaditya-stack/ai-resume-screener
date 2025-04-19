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
                    "JPA",
                    "Hibernate",
                    "Maven",
                    "Gradle",
                    "JUnit",
                    "Mockito",
                    "Java 8+",
                    "Microservices",
                ],
            },
            {
                "name": "Cloud & DevOps",
                "weight": 8,
                "terms": [
                    "AWS",
                    "Docker",
                    "Kubernetes",
                    "CI/CD",
                    "Jenkins",
                    "Azure",
                    "GCP",
                    "Cloud Native",
                ],
            },
            {
                "name": "Database Technologies",
                "weight": 8,
                "terms": [
                    "Oracle",
                    "PostgreSQL",
                    "MySQL",
                    "MongoDB",
                    "Cassandra",
                    "Redis",
                    "NoSQL",
                ],
            },
            {
                "name": "Integration & Messaging",
                "weight": 7,
                "terms": [
                    "Kafka",
                    "RabbitMQ",
                    "ActiveMQ",
                    "Apache Camel",
                    "WebSockets",
                    "gRPC",
                ],
            },
            {
                "name": "Security",
                "weight": 7,
                "terms": [
                    "OAuth",
                    "JWT",
                    "Spring Security",
                    "Keycloak",
                    "Authentication",
                    "Authorization",
                ],
            },
            {
                "name": "Performance & Monitoring",
                "weight": 6,
                "terms": [
                    "JVM Tuning",
                    "Profiling",
                    "ELK Stack",
                    "Prometheus",
                    "Grafana",
                    "New Relic",
                    "AppDynamics",
                ],
            },
            {
                "name": "Architecture Patterns",
                "weight": 6,
                "terms": [
                    "DDD",
                    "CQRS",
                    "Event Sourcing",
                    "Design Patterns",
                    "Clean Architecture",
                    "Hexagonal Architecture",
                ],
            },
            {
                "name": "Frontend Technologies",
                "weight": 4,
                "terms": [
                    "Angular",
                    "React",
                    "TypeScript",
                    "JavaScript",
                    "HTML",
                    "CSS",
                ],
            },
            {
                "name": "Project Management",
                "weight": 4,
                "terms": [
                    "Agile",
                    "Scrum",
                    "Jira",
                    "Confluence",
                    "Team Leadership",
                    "Mentoring",
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
Senior Java Developer Position

Experience Required: 3+ years

Required Technical Skills:
- Strong proficiency in Java and its ecosystem
- Sound knowledge of Object-Oriented Programming (OOP) patterns and concepts
- Experience with different design and architectural patterns
- Good understanding of MVC pattern and JDBC
- Version control systems like Git and SVN
- SQL proficiency
- Continuous integration expertise

Additional Technical Requirements:
- Java Server Pages (JSP) and Servlets
- Spring and Struts frameworks
- SOAP Web Services and OpenSPML
- Web technologies: HTML, JavaScript, CSS, jQuery
- Data formats: XML, JSON
- Multithreading and synchronization concepts
"""

__MOCK_LLM_MODE__ = True
