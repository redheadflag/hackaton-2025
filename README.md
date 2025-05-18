# Nature Lover

Our project reflects the noble intentions of modern society, such as caring for the Earth and maintaining a sustainable environment. Additionally, it provides nature enthusiasts with a means to earn a living while pursuing their passion, thereby enhancing their quality of life. Furthermore, our solution encourages companies and businesses to adopt more responsible practices in matters of nature and ecology.

## Overview
This platform enables users to create and join channels dedicated to ecological topics, share geolocated messages, and collaborate on environmental initiatives. It is designed to foster a community of nature lovers, experts, and organizations working together for a greener future.

## Features
- **User Management**: Register as a human or robot user, with support for oracles (trusted users).
- **Channels**: Create public or private channels for focused discussions and collaboration.
- **Geolocated Messaging**: Share messages with geospatial data (latitude/longitude), enabling location-based discussions and reporting.
- **Role System**: Differentiate between humans, robots, and oracles to support trust and automation.
- **API-First**: Built with FastAPI for high performance and easy integration.

### Technical Details
- **Backend**: Python 3.13, FastAPI, SQLAlchemy (async), Alembic for migrations.
- **Database**: PostgreSQL with PostGIS extension for geospatial data.
- **Authentication**: Passwords are securely hashed using bcrypt via Passlib.
- **Geospatial Support**: Messages include geolocation using GeoAlchemy2 and Shapely.
- **Containerization**: Docker and Docker Compose for easy deployment.
- **Configuration**: Managed via Pydantic settings and .env files.
- **Testing & Development**: Hot-reloading and development workflow supported via Docker Compose.
