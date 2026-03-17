from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class ReportBuilder:
    """Orchestrates the creation of PDF, DOCX, or HTML reports using Jinja2."""
    
    def __init__(self, template_dir: str = "templates"):
        # Real implementation would point to the bundled templates folder
        local_dir = Path(__file__).parent / template_dir
        local_dir.mkdir(parents=True, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(str(local_dir)))
        
    def build_report(self, results: dict, output_format: str = "html", output_path: str = "report.html"):
        """Generates the final report applying the formatted results to a template."""
        # This is a mockup of the actual rendering process
        template_name = f"html_report.j2" if output_format == "html" else f"apa7.{output_format}.j2"
        
        # We simulate the file writing here to avoid requiring the actual jinja files for the MVP build
        with open(output_path, "w") as f:
            f.write(f"<h1>StatForge Report</h1>\n<p>Generated {output_format} output.</p>\n")
            f.write("<h2>Methods</h2>\n<p>{}</p>\n".format(results.get("methods_text", "")))
        
        return output_path
