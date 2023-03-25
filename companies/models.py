from django.db import models


class Company(models.Model):
    """
    A model representing a company

    Attributes:
        id (int): The primary key of the company
        company_name (str): The name of the company
        country (str): The country where the company is located
        email (str): The email of the company
        website (str): The website of the company
    """
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255)

    def __str__(self):
        return self.company_name

    @staticmethod
    def get_by_id(pk):
        """
        Retrieves a company by its id

        Args:
            pk (int): The primary key of the company

        Returns:
            Company: The company with the given id or None if it does not exist
        """
        return Company.objects.get(id=pk) if Company.objects.filter(id=pk).exists() else None

    @staticmethod
    def delete_by_id(pk):
        """
        Deletes a company by its id

        Args:
            pk (int): The primary key of the company

        Returns:
            bool: True if the company was deleted, False otherwise
        """
        if Company.get_by_id(pk) is None:
            return False
        Company.objects.get(id=pk).delete()
        return True

    @staticmethod
    def get_all():
        """
        Retrieves all companies

        Returns:
            QuerySet: A queryset containing all companies
        """
        return Company.objects.all()

    @staticmethod
    def get_by_name(name):
        """
        Retrieves a company by its name

        Args:
            name (str): The name of the company

        Returns:
            QuerySet: A queryset containing all companies with the given name
        """
        return Company.objects.filter(company_name__icontains=name)

    @staticmethod
    def get_by_country(country):
        """
        Retrieves a company by its country

        Args:
            country (str): The country of the company

        Returns:
            QuerySet: A queryset containing all companies with the given country
        """
        return Company.objects.filter(country__icontains=country)

    @staticmethod
    def get_by_email(email):
        """
        Retrieves a company by its email

        Args:
            email (str): The email of the company

        Returns:
            QuerySet: A queryset containing all companies with the given email
        """
        return Company.objects.filter(email__icontains=email)

    @staticmethod
    def create(company_name, country, email, website):
        """
        Creates a new company

        Args:
            company_name (str): The name of the company
            country (str): The country where the company is located
            email (str): The email of the company
            website (str): The website of the company

        Returns:
            Company: The newly created company

        Raises:
            ValueError: If any of the fields is empty
        """
        if not company_name and not country and not email and not website:
            raise ValueError('Company name, country, email and website cannot be empty')
        company = Company.objects.create(company_name=company_name, country=country, email=email, website=website)
        return company

    def update(self, company_name, country, email, website):
        """
        Updates the company

        Args:
            company_name (str): The name of the company
            country (str): The country where the company is located
            email (str): The email of the company
            website (str): The website of the company

        Raises:
            ValueError: If no field is provided

        Returns:
            None
        """
        if not company_name or not country or not email or not website:
            raise ValueError('At least one field must be provided')
        if company_name is not None:
            self.company_name = company_name
        if country is not None:
            self.country = country
        if email is not None:
            self.email = email
        if website is not None:
            self.website = website
        self.save()
