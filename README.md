Deploy an Article CMS to Azure

<i>Cloud Developer using Microsoft Azure Nanodegree Program</i>

A simple Content Management System (CMS) for articles, where a user can log in, view published articles, and publish new articles.

My Udacity Project (Azure Applications) Overview

In this project, I deployed a CMS for articles where users can log in, view articles, and publish new articles. Each article includes a title, author, body, and an image. Text data is stored in Azure SQL Server, and images are stored in Azure Blob Storage.

The CMS components I implemented include:

Web app using Python with Flask.

SQL database with user and article tables.

Blob Storage container for storing images.

Microsoft Authentication for Sign in with Microsoft.

Logging for both successful and unsuccessful login attempts.

I fully managed all Azure resources to deploy the app and set up the workflow for continuous deployment via GitHub.

App examples for the project were based on the starter code provided here
.

Specifications Completed

I completed all project specifications, which are documented in files and screenshots here
. Reference the screenshots above for a walkthrough showing the project deployed on Azure.

<img src="https://github.com/kathleenwest/article-cms-azure-demo-project/blob/main/demo/MeetsSpecifications.jpg">
Project Instructions

To complete this project, I performed the following steps:

Created a Resource Group in Azure.

Created an SQL Database with user and article tables, populated using provided scripts.

Created a Blob Storage Container for images and confirmed endpoints.

Added functionality for Sign In with Microsoft using the msal library and Azure AD registration.

Chose Azure App Service (instead of a VM) to deploy the Flask app for lower cost, easier maintenance, built-in scaling, and GitHub integration.

Added logging for login attempts in __init__.py and views.py.

Tested app functionality: logged in, created an article with title “Hello World!”, author “Jane Doe”, added a body and image, and confirmed it saved successfully.

Captured a screenshot of the Azure Resource Group showing all created resources.

Captured a screenshot of Redirect URIs for Microsoft Authentication.

Captured logs showing both invalid and successful login attempts.

Deployment Choice: VM vs App Service

I chose Azure App Service because:

It is lower cost than a VM.

Requires less maintenance, with no OS or security configuration overhead.

Integrates directly with GitHub for fast, automated deployment.

Offers high availability and reliability without manual management.

Provides scalable options suitable for the app size.

I would consider a VM only if the app needed custom OS setups, heavy background processing, advanced networking, or strict security requirements. For this CMS, App Service was the most efficient choice.

Project Submission

My submission includes:

Screenshot of an article created in the CMS on Azure, showing the URL and uploaded image.

Screenshot of the Azure Resource Group with all resources.

Screenshot of the SQL tables with populated data.

Screenshot of the Blob Storage endpoints.

Screenshot of Redirect URIs for Microsoft Authentication.

Screenshot of logs showing both invalid and successful login attempts.

Updated application code (__init__.py and views.py).

WRITEUP.md analyzing the VM vs App Service decision.

OPTIONAL: URL to the deployed Python App Service.
