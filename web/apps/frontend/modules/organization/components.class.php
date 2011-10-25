<?php

class organizationComponents extends sfComponents {

  public function executeSidebar(sfWebRequest $request)
  {
    $this->organizations = Doctrine_Core::getTable('Organization');
    $organizationID = $request->getParameter("organization");
    if (strlen($organizationID) > 0 && ctype_digit($organizationID)) {
        $this->organizationID = $organizationID;
    }
  }
}

?>
