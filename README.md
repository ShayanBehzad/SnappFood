# SnappFood Project

Welcome to the SnappFood Clone project! This project is a comprehensive food delivery platform, inspired by the popular SnappFood app.that offers separate sections for sellers and customers, each with a unique set of features designed for an efficient experience.
It provides a seamless experience for managing food listings, processing orders, updating inventory, and generating reports. The platform ensures secure and efficient transactions between restaurants and customers.The project is deployed using Nginx and Gunicorn, and it can be accessed at [www.shayanbehzad.ir/snappfood/register/](http://www.shayanbehzad.ir/snappfood/register/).

## Features

### Seller Section

- **Food Management:** Sellers can manage their food listings, including adding, updating, and removing items from their inventory.
- **Order Management:** Sellers can view all incoming orders, update the status of orders, and manage order processing through a streamlined dashboard.
- **Order Statuses:** Orders can be set to `Pending`, `Preparing`, `Sent`, or `Delivered`. Once an order is marked as `Delivered`, it is automatically removed from the dashboard and can be accessed in the reports section.
- **Reports:** A dedicated reports page allows sellers to view delivered orders with date filtering for better insights and record-keeping.
- **Registration & Authentication:** Sellers register through a secure, token-based system. Upon successful registration, they receive a welcome email sent asynchronously using Celery and Redis.
- **Dashboard:** After registration, sellers are redirected to a dashboard where they can manage all undelivered orders and update their status as needed.

### Customer Section

- **Registration & Authentication:** Customers can securely register and authenticate via a REST API.
- **Restaurant & Food Browsing:** Customers can view available restaurants and their food listings.
- **Order Cart:** Customers can create and submit order carts with their selected items.
- **Comments & Ratings:** Customers can post comments on restaurants and rate their experiences.
- **Order Management:** Customers can view and manage their orders through a secure and efficient interface.

## Deployment

The project is deployed using Nginx and Gunicorn for robust performance and scalability.

Visit the project at [www.shayanbehzad.ir/snappfood/register/](http://www.shayanbehzad.ir/snappfood/register/).

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Asynchronous Task Queue**: Celery with Redis
- **Deployment**: Nginx, Gunicorn
- **Version Control**: Git
