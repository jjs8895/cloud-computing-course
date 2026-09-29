import functions_framework


@functions_framework.http
def portfolio(request):
    """HTTP Cloud Function serving a lightweight personal portfolio."""

    if request.args.get("format") == "json":
        return {
            "name": "Job Sava",
            "program": "Computer Engineering @ Rochester Institute of Technology",
            "focus": [
                "Embedded Systems",
                "Embedded Linux",
                "Low-Level Software",
                "Cloud Computing",
            ],
            "skills": [
                "C",
                "Python",
                "Linux",
                "ARM",
                "STM32",
                "Embedded Linux",
                "Yocto",
                "Git",
                "GitHub",
            ],
            "projects": [
                {
                    "name": "Adjustable Pediatric Prosthetic",
                    "description": (
                        "Embedded system and custom PCB for an electrically "
                        "adjustable pediatric prosthetic device."
                    ),
                },
                {
                    "name": "Embedded Linux Development",
                    "description": (
                        "Linux kernel, U-Boot, Yocto, device tree, and "
                        "hardware debugging on TI-based embedded platforms."
                    ),
                },
                {
                    "name": "Cloud Computing",
                    "description": (
                        "Coursework exploring distributed systems, cloud "
                        "infrastructure, virtualization, and serverless computing."
                    ),
                },
            ],
            "links": {
                "github": "https://github.com/jjs8895",
                "linkedin": "YOUR_LINKEDIN_URL",
            },
        }

    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Job Sava | Embedded Systems Engineer</title>

    <meta
        name="description"
        content="Job Sava — Computer Engineering student focused on embedded systems, Linux, and low-level software."
    >

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        :root {
            --bg: #080b10;
            --bg-secondary: #0d1219;
            --card: rgba(18, 25, 34, 0.72);
            --border: rgba(255, 255, 255, 0.09);
            --text: #f1f5f9;
            --muted: #94a3b8;
            --accent: #4ade80;
            --accent-secondary: #22d3ee;
            --accent-dark: #14532d;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            background:
                radial-gradient(
                    circle at 80% 10%,
                    rgba(34, 211, 238, 0.08),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 10% 30%,
                    rgba(74, 222, 128, 0.07),
                    transparent 28%
                ),
                var(--bg);

            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: 0.035;

            background-image:
                linear-gradient(
                    rgba(255, 255, 255, 0.5) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(255, 255, 255, 0.5) 1px,
                    transparent 1px
                );

            background-size: 45px 45px;
            mask-image: linear-gradient(
                to bottom,
                black,
                transparent 80%
            );
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        .container {
            width: min(1100px, 90%);
            margin: auto;
        }

        /* Navigation */

        nav {
            position: sticky;
            top: 0;
            z-index: 10;

            backdrop-filter: blur(16px);
            background: rgba(8, 11, 16, 0.78);
            border-bottom: 1px solid var(--border);
        }

        .nav-inner {
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo {
            font-family: monospace;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--accent);
        }

        .logo::before {
            content: "> ";
            color: var(--accent-secondary);
        }

        .nav-links {
            display: flex;
            gap: 28px;
            list-style: none;
            color: var(--muted);
            font-size: 0.9rem;
        }

        .nav-links a {
            transition: color 0.2s ease;
        }

        .nav-links a:hover {
            color: var(--accent);
        }

        /* Hero */

        .hero {
            min-height: 88vh;
            display: flex;
            align-items: center;
            padding: 90px 0;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 70px;
            align-items: center;
        }

        .eyebrow {
            color: var(--accent);
            font-family: monospace;
            font-size: 0.9rem;
            margin-bottom: 18px;
        }

        h1 {
            font-size: clamp(3.3rem, 8vw, 6.5rem);
            line-height: 0.95;
            letter-spacing: -0.06em;
            margin-bottom: 28px;
        }

        .gradient-text {
            background: linear-gradient(
                90deg,
                var(--accent),
                var(--accent-secondary)
            );

            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .hero-description {
            color: var(--muted);
            max-width: 620px;
            font-size: 1.15rem;
            margin-bottom: 32px;
        }

        .buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
        }

        .button {
            padding: 12px 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-weight: 600;
            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                background 0.2s ease;
        }

        .button:hover {
            transform: translateY(-2px);
            border-color: var(--accent);
        }

        .button-primary {
            background: var(--accent);
            color: #041008;
            border-color: var(--accent);
        }

        .button-primary:hover {
            background: #86efac;
        }

        /* Terminal */

        .terminal {
            background: rgba(9, 14, 20, 0.88);
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            box-shadow:
                0 25px 80px rgba(0, 0, 0, 0.4),
                0 0 50px rgba(74, 222, 128, 0.04);
        }

        .terminal-bar {
            display: flex;
            align-items: center;
            gap: 7px;
            padding: 13px 16px;
            border-bottom: 1px solid var(--border);
        }

        .dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #475569;
        }

        .terminal-title {
            margin-left: auto;
            margin-right: auto;
            font-family: monospace;
            font-size: 0.75rem;
            color: #64748b;
        }

        .terminal-body {
            padding: 25px;
            font-family: monospace;
            font-size: 0.85rem;
            color: #cbd5e1;
        }

        .terminal-line {
            margin-bottom: 12px;
        }

        .prompt {
            color: var(--accent);
        }

        .command {
            color: var(--accent-secondary);
        }

        .comment {
            color: #64748b;
        }

        .cursor {
            display: inline-block;
            width: 8px;
            height: 15px;
            background: var(--accent);
            vertical-align: middle;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            50% {
                opacity: 0;
            }
        }

        /* Sections */

        section {
            padding: 100px 0;
        }

        .section-label {
            font-family: monospace;
            color: var(--accent);
            font-size: 0.85rem;
            margin-bottom: 10px;
        }

        h2 {
            font-size: clamp(2rem, 5vw, 3rem);
            letter-spacing: -0.04em;
            margin-bottom: 18px;
        }

        .section-intro {
            color: var(--muted);
            max-width: 650px;
            margin-bottom: 45px;
        }

        /* About */

        .about-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 30px;
            backdrop-filter: blur(10px);
        }

        .card p {
            color: var(--muted);
        }

        /* Skills */

        .skills {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .skill {
            padding: 9px 14px;
            border: 1px solid var(--border);
            border-radius: 7px;
            background: rgba(255, 255, 255, 0.025);
            color: #cbd5e1;
            font-family: monospace;
            font-size: 0.85rem;
        }

        .skill:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        /* Projects */

        .projects {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .project {
            position: relative;
            overflow: hidden;
            transition:
                transform 0.25s ease,
                border-color 0.25s ease;
        }

        .project:hover {
            transform: translateY(-6px);
            border-color: rgba(74, 222, 128, 0.35);
        }

        .project-number {
            font-family: monospace;
            color: var(--accent);
            font-size: 0.8rem;
            margin-bottom: 25px;
        }

        .project h3 {
            font-size: 1.3rem;
            margin-bottom: 12px;
        }

        .project p {
            color: var(--muted);
            font-size: 0.95rem;
        }

        /* Contact */

        .contact {
            text-align: center;
            max-width: 700px;
            margin: auto;
        }

        .contact p {
            color: var(--muted);
            margin-bottom: 30px;
        }

        .links {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        /* Footer */

        footer {
            border-top: 1px solid var(--border);
            padding: 30px 0;
            color: #64748b;
            font-family: monospace;
            font-size: 0.75rem;
        }

        .footer-inner {
            display: flex;
            justify-content: space-between;
            gap: 20px;
        }

        /* Mobile */

        @media (max-width: 800px) {
            .hero-grid,
            .about-grid,
            .projects {
                grid-template-columns: 1fr;
            }

            .hero {
                min-height: auto;
                padding: 90px 0 60px;
            }

            .terminal {
                margin-top: 20px;
            }

            .nav-links {
                display: none;
            }

            section {
                padding: 70px 0;
            }

            .footer-inner {
                flex-direction: column;
            }
        }
    </style>
</head>

<body>

<nav>
    <div class="container nav-inner">
        <a href="#" class="logo">job_sava</a>

        <ul class="nav-links">
            <li><a href="#about">About</a></li>
            <li><a href="#skills">Skills</a></li>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </div>
</nav>


<main>

    <!-- HERO -->

    <section class="hero">
        <div class="container hero-grid">

            <div>
                <div class="eyebrow">
                    COMPUTER ENGINEERING • EMBEDDED SYSTEMS
                </div>

                <h1>
                    Building software
                    <span class="gradient-text">close to the metal.</span>
                </h1>

                <p class="hero-description">
                    I'm Job Sava, a Computer Engineering student at RIT
                    interested in embedded systems, Linux, operating systems,
                    and low-level software development.
                </p>

                <div class="buttons">
                    <a class="button button-primary" href="#projects">
                        View my work →
                    </a>

                    <a class="button" href="#contact">
                        Get in touch
                    </a>
                </div>
            </div>


            <div class="terminal">

                <div class="terminal-bar">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>

                    <span class="terminal-title">
                        job@portfolio: ~
                    </span>
                </div>

                <div class="terminal-body">

                    <div class="terminal-line">
                        <span class="prompt">$</span>
                        <span class="command">whoami</span>
                    </div>

                    <div class="terminal-line">
                        job_sava
                    </div>

                    <div class="terminal-line">
                        <span class="prompt">$</span>
                        <span class="command">cat interests.txt</span>
                    </div>

                    <div class="terminal-line">
                        embedded systems<br>
                        embedded linux<br>
                        operating systems<br>
                        low-level software
                    </div>

                    <div class="terminal-line">
                        <span class="prompt">$</span>
                        <span class="command">echo $STATUS</span>
                    </div>

                    <div class="terminal-line">
                        building things that work.
                        <span class="cursor"></span>
                    </div>

                </div>

            </div>

        </div>
    </section>


    <!-- ABOUT -->

    <section id="about">

        <div class="container">

            <div class="section-label">01 / ABOUT</div>

            <h2>Hardware meets software.</h2>

            <p class="section-intro">
                I enjoy working where software interacts directly with
                hardware — from microcontrollers and custom PCBs to Linux
                kernels and embedded operating systems.
            </p>


            <div class="about-grid">

                <div class="card">

                    <h3>Education</h3>

                    <p>
                        Currently studying Computer Engineering at the
                        Rochester Institute of Technology, with interests
                        spanning embedded software, computer architecture,
                        operating systems, and cloud computing.
                    </p>

                </div>


                <div class="card">

                    <h3>What I like building</h3>

                    <p>
                        Embedded systems, Linux-based devices, hardware
                        interfaces, custom electronics, and software that
                        connects the physical world to computing systems.
                    </p>

                </div>

            </div>

        </div>

    </section>


    <!-- SKILLS -->

    <section id="skills">

        <div class="container">

            <div class="section-label">02 / TOOLBOX</div>

            <h2>Things I work with.</h2>

            <p class="section-intro">
                A mix of software, hardware, and systems tools used across
                coursework, projects, and engineering experience.
            </p>

            <div class="skills">

                <span class="skill">C</span>
                <span class="skill">Python</span>
                <span class="skill">Linux</span>
                <span class="skill">Git</span>
                <span class="skill">ARM</span>
                <span class="skill">STM32</span>
                <span class="skill">Embedded Linux</span>
                <span class="skill">Yocto</span>
                <span class="skill">U-Boot</span>
                <span class="skill">Device Tree</span>
                <span class="skill">RTOS</span>
                <span class="skill">PCB Design</span>
                <span class="skill">KiCad</span>
                <span class="skill">MATLAB</span>
                <span class="skill">Verilog</span>
                <span class="skill">SystemVerilog</span>

            </div>

        </div>

    </section>


    <!-- PROJECTS -->

    <section id="projects">

        <div class="container">

            <div class="section-label">03 / PROJECTS</div>

            <h2>Things I've worked on.</h2>

            <p class="section-intro">
                A few projects and areas of experience that represent my
                interests in embedded and systems engineering.
            </p>


            <div class="projects">

                <article class="card project">

                    <div class="project-number">PROJECT_01</div>

                    <h3>
                        Adjustable Pediatric Prosthetic
                    </h3>

                    <p>
                        Designed the electrical architecture and custom PCB
                        for an electrically adjustable pediatric prosthetic
                        device using an STM32 microcontroller, pressure
                        sensing, air pumps, and motor control.
                    </p>

                </article>


                <article class="card project">

                    <div class="project-number">PROJECT_02</div>

                    <h3>
                        Embedded Linux
                    </h3>

                    <p>
                        Worked with embedded Linux platforms involving Linux
                        kernel upgrades, U-Boot, Yocto, device trees,
                        peripheral validation, networking, and hardware
                        debugging.
                    </p>

                </article>


                <article class="card project">

                    <div class="project-number">PROJECT_03</div>

                    <h3>
                        Cloud Computing
                    </h3>

                    <p>
                        Coursework exploring cloud infrastructure,
                        distributed systems, virtualization, and
                        serverless computing using cloud platforms.
                    </p>

                </article>

            </div>

        </div>

    </section>


    <!-- CONTACT -->

    <section id="contact">

        <div class="container">

            <div class="card contact">

                <div class="section-label">04 / CONNECT</div>

                <h2>Let's build something.</h2>

                <p>
                    Interested in embedded systems, Linux, or low-level
                    software? Check out my work or connect with me online.
                </p>

                <div class="links">

                    <a
                        class="button button-primary"
                        href="https://github.com/jjs8895"
                        target="_blank"
                    >
                        GitHub ↗
                    </a>

                    <a
                        class="button"
                        href="YOUR_LINKEDIN_URL"
                        target="_blank"
                    >
                        LinkedIn ↗
                    </a>

                </div>

            </div>

        </div>

    </section>

</main>


<footer>

    <div class="container footer-inner">

        <span>
            © 2026 Job Sava
        </span>

        <span>
            Deployed with Google Cloud Functions
        </span>

    </div>

</footer>

</body>
</html>
"""

    return html
