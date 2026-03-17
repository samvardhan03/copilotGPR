# Services & Monetization

StatForge is built to provide rigorous, automated statistical reporting to both independent researchers and scale-out institutional labs. 

We offer six distinct deployment and analysis tiers.

## 1. Open Source (Free)
The core CLI provides free, unrestricted access to the frequentist model suite.
*   **Included:** Full CLI `statforge run` pipeline execution, frequentist models, and APA PDF/DOCX/HTML output formats.
*   **Narrative Generation:** Local LLM execution via Ollama. 

## 2. Research Pro ($79/month)
For researchers needing specialized journal formats without local hardware constraints.
*   **Included:** Cloud-hosted LLM narratives, negating local execution requirements. Includes the complete suite of journal templates (e.g., Nature, PLOS ONE, IEEE, NEJM).
*   **Support:** Priority email support.

## 3. One-Time Analysis ($299 – $799)
For graduate students or researchers requiring immediate, verified execution of a singular dataset.
*   **Process:** Upload your parsed `.csv` or `.sav` file. Our team executes the correct Bayesian or Frequentist pipeline.
*   **Included:** We deliver the complete PDF report and the explicit `statforge_config.yaml` guaranteeing analytical reproducibility.

## 4. Custom Model Build ($800 – $2,500)
For researchers needing specific analytical architectures missing from the default `@register` suite.
*   **Process:** After scoping the analytical question, we build a bespoke PyMC model deployed as a `.py` plugin for your `~/.statforge/plugins/` directory.
*   **Included:** A prior consultation, sensitivity analysis logic embedded within the model, and complete methodological documentation.

## 5. Lab Deployment ($3,000 – $8,000)
For principal investigators seeking to standardize output across an entire research group.
*   **Process:** Server or Cloud environment installation of the StatForge engine.
*   **Included:** Custom institutional templates, an LLM backend configuration, a 2-hour onboarding session (for up to 5 researchers), and 1-year of dedicated technical support.

## 6. Institutional License ($12,000+/year)
For university-wide or corporate biostatistics alignment.
*   **Process:** Full integration across departments with dedicated SLA.
*   **Included:** Unlimited researchers, Single Sign-On (SSO/LDAP), dedicated Slack support (< 24h response), quarterly model updates, and branded templates.

---

## Purchasing & License Configuration

We utilize a self-serve Stripe Checkout flow to issue license keys instantly for tiers up to $799.

### Workflow:

1.  **Checkout**: Navigate to the [StatForge Landing Page](index.html) and select your desired tier via the Stripe link.
2.  **Key Issuance**: Upon payment verification, a webhook automatically generates a unique `license_key` (UUID4) and emails it to your registered address.
3.  **Local Configuration**: 
    Store the key by defining the environment variable in your `.bashrc` or `.zshrc`:
    ```bash
    export STATFORGE_LICENSE_KEY="your-uuid4-key"
    ```
    Alternatively, inject it manually into your `~/.statforge/statforge_config.yaml`.
4.  **Validation**: Future invocations of `statforge run` will automatically hit the lightweight validation endpoint to unlock specific template features and cloud environments.
