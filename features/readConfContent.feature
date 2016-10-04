# features/readConfContent.feature
@initialize @confRead

Feature: Read and convert confluence wiki page content
  As a confluence user
  I want to read a specific wiki page
  So that I can extract the content and convert it to Latex format

  @readConfWikiContent
  Scenario: Read a confluence wiki page
    Given I have Confluence user credentials
    When I look for a wiki page with a specific title
    Then I want the be able to extract the content

  @convertContenttoTex
  Scenario: Convert wiki page HTML to Tex
    Given I have a Confluence page wiki content
    When the content is converted to a workable tex format
    Then sanitize the content to be ready for final document format
