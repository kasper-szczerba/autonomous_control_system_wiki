---
icon: lucide/clipboard-clock
---

# Changelog

This page documents the changes made to the Autonomous Control System project. It includes updates to the codebase, documentation, and any other relevant modifications.

## New Documentation Structure

**21-05-2026**

The documentation has been restructured to provide a clearer and more organized view of the project. The new structure includes separate sections for the codebase, architecture, components, and other relevant topics. This change was made to improve the readability and accessibility of the documentation for both new and existing contributors.

## Additional Interfaces for Vision Detectors

**21-05-2026**

The vision subsystem has been expanded with new interfaces for the floor and obstacle detectors. These interfaces extend the existing `i_threaded_component` interface and provide methods for retrieving detection results, such as the detected floor plane, obstacle contours, and their respective coefficients.

This change was necessary to prepare for the implementation of unit tests and mocking of these components, allowing for better testability and separation of concerns in the codebase.

## The docs are live!

**21-05-2026**

The documentation is now live! You can explore the codebase, understand the architecture, and learn about the various components of the Autonomous Control System. We will continue to update the documentation as we make progress on the project, so stay tuned for more updates!

[Explore the codebase documentation](../codebase/index.md) to see the latest changes and additions to the project.
