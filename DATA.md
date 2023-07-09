# Data

This README.md is a guide to understanding the Space Exploration data model used in this FastAPI example
and the associated fixtures.

## The Data Model

The data model consists of three main entities:

1. Space Agencies
2. Launching Sites
3. Satellites

### 1. Space Agencies

A space agency represents an organization that has capabilities of launching satellites into space.
This entity consists of the following properties:

- `id` (UUID): A unique identifier for the agency.
- `name` (string): The name of the space agency.
- `description` (string): A brief description about the space agency.
- `website` (string): The URL of the agency's official website.
- `active` (boolean): Indicates whether the agency is currently active.

### 2. Launching Sites

A launching site is a location from where space agencies launch their satellites.
This entity consists of the following properties:

- `id` (UUID): A unique identifier for the launching site.
- `name` (string): The name of the launching site.
- `description` (string): A brief description about the launching site.
- `country` (string): The country where the launching site is located.
- `address` (string): The address of the launching site.
- `agency_ids` (list of UUIDs): A list of unique identifiers of space agencies that use this launching site.
- `avg_rating` (float): An average rating representing the site's performance or reputation.

### 3. Satellites

A satellite is an object that has been intentionally placed into orbit.
In this model, a satellite represents one launched by a space agency from a specific launching site.
This entity consists of the following properties:

- `id` (UUID): A unique identifier for the satellite.
- `name` (string): The name of the satellite.
- `launch_date` (string): The date the satellite was launched.
- `status` (string): Current status of the satellite (e.g., "active", "inactive", "decommissioned").
- `agency_id` (UUID): The unique identifier of the space agency that launched the satellite.
- `launching_site_id` (UUID): The unique identifier of the launching site from where the satellite was launched.

## Fixtures

Fixtures are sets of data to be imported into a local database or used to run unit tests.
The data model uses three fixtures, each corresponding to one of our entities.

- `space_agencies.json`: a list of space agencies.
- `launching_sites.json`: a list of launching sites, each linked to the space agencies that use them. A launching site can be shared by different space agencies.
- `satellites.json`: a list of satellites, each linked to a space agency and launching site.

The data in these fixtures are for illustrative purposes and should be replaced with actual data for a production environment. The relationships among the data (e.g., satellites are linked to agencies and launching sites) are representative of real-world relationships in the domain of space exploration.
