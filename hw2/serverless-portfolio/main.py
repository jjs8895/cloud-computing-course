import functions_framework


@functions_framework.http
def portfolio(request):
    """HTTP Cloud Function for a lightweight personal portfolio."""

    if request.args.get("format") == "json":
        return {
            "name": "Job Sava",
            "program": "Computer Engineering, Rochester Institute of Technology",
            "bio": (
                "Computer Engineering student interested in embedded systems, "
                "Linux, operating systems, and low-level software development."
            ),
            "skills": [
                "C",
                "Python",
                "Linux",
                "Embedded Systems",
                "ARM",
                "STM32",
                "Git"
            ],
            "projects": [
                "Adjustable Pediatric Prosthetic Device",
                "Embedded Linux Development",
                "Cloud Computing Coursework"
            ],
            "links": {
                "github": "https://github.com/jjs8895",
                "linkedin": "www.linkedin.com/in/job-sava"
            }
        }

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Sava | Computer Engineering</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 40px 20px;
                line-height: 1.6;
                color: #222;
            }

            header {
                margin-bottom: 40px;
            }

            h1 {
                margin-bottom: 5px;
            }

            h2 {
                margin-top: 35px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }

            .subtitle {
                color: #666;
                font-size: 1.1rem;
            }

            .skills {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                padding: 0;
                list-style: none;
            }

            .skills li {
                background: #eee;
                padding: 5px 10px;
                border-radius: 4px;
            }

            a {
                color: #0066cc;
            }

            footer {
                margin-top: 50px;
                color: #777;
                font-size: 0.9rem;
            }
        </style>
    </head>

    <body>
        <header>
            <h1>Job Sava</h1>
            <p class="subtitle">
                Computer Engineering Student | Embedded Systems & Linux
            </p>
        </header>

        <section>
            <h2>About Me</h2>
            <p>
                I am a Computer Engineering student at the Rochester Institute
                of Technology interested in embedded systems, Linux, operating
                systems, and low-level software development. I enjoy working
                close to the hardware and developing software that connects
                embedded hardware with higher-level systems.
            </p>
        </section>

        <section>
            <h2>Skills & Interests</h2>
            <ul class="skills">
                <li>C</li>
                <li>Python</li>
                <li>Linux</li>
                <li>Embedded Systems</li>
                <li>ARM</li>
                <li>STM32</li>
                <li>Git</li>
            </ul>
        </section>

        <section>
            <h2>Projects & Experience</h2>

            <h3>Adjustable Pediatric Prosthetic Device</h3>
            <p>
                Computer engineering work on an electrically adjustable
                pediatric prosthetic device using embedded control,
                pressure sensors, air pumps, and a custom PCB.
            </p>

            <h3>Embedded Linux Development</h3>
            <p>
                Worked with embedded Linux systems, including Linux kernels,
                U-Boot, Yocto, device trees, drivers, and hardware
                debugging.
            </p>

            <h3>Cloud Computing</h3>
            <p>
                Coursework involving cloud computing, virtualization,
                distributed systems, and serverless application deployment.
            </p>
        </section>

        <section>
            <h2>Links</h2>
            <p>
                <a href="https://github.com/jjs8895" target="_blank">
                    GitHub
                </a>
            </p>
            <p>
                <a href="www.linkedin.com/in/job-sava" target="_blank">
                    LinkedIn
                </a>
            </p>
        </section>

        <footer>
            <p>Portfolio deployed using Google Cloud Functions (2nd gen).</p>
        </footer>
    </body>
    </html>
    """

    return html
