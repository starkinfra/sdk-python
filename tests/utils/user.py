import os
import starkinfra


bank_code = os.environ["SANDBOX_BANK_CODE"]
template_id = os.environ["SANDBOX_TEMPLATE_ID"]

exampleProject = starkinfra.Project(
    environment="sandbox",
    id=os.environ["SANDBOX_INFRA_ID"],
    private_key=os.environ["SANDBOX_INFRA_PRIVATE_KEY"],
)

exampleOrganization = starkinfra.Organization(
    environment="sandbox",
    id=os.environ["SANDBOX_ORGANIZATION_ID"],  # "8888888888888888"
    private_key=os.environ["SANDBOX_ORGANIZATION_PRIVATE_KEY"],  # "-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEIBEcEJZLk/DyuXVsEjz0w4vrE7plPXhQxODvcG1Jc0WToAcGBSuBBAAK\noUQDQgAE6t4OGx1XYktOzH/7HV6FBukxq0Xs2As6oeN6re1Ttso2fwrh5BJXDq75\nmSYHeclthCRgU8zl6H1lFQ4BKZ5RCQ==\n-----END EC PRIVATE KEY-----"
)

assert exampleProject.environment != "production", "NEVER RUN THE TEST ROUTINE IN PRODUCTION"
