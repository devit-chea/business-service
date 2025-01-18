class ModelFieldChoices:
        
    METHOD_TYPE = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('credit_card', 'Credit Card')
    ]
    
class CompanyType:
    COMPANY = "company"
    BRANCH  = "branch"
    
OFFICE_TYPE = [
    (CompanyType.COMPANY, "Company"),
    (CompanyType.BRANCH, "Branch"),
]