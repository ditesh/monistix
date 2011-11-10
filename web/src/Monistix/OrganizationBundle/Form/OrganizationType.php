<?php

namespace Monistix\OrganizationBundle\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilder;

class OrganizationType extends AbstractType {

    public function buildForm(FormBuilder $builder, array $options) {

        $builder->add("name", "text")
                ->add("accounts_active", "checkbox", array("required"=>false))
                ->add("hosts_active", "checkbox", array("required"=>false))
                ->add("enable_billing", "checkbox", array("required"=>false))
                ->add("max_hosts", "integer", array("required"=>false))
                ->add("max_accounts", "integer", array("required"=>false))
                ->add("contact_name", "text", array("required"=>false))
                ->add("contact_number", "text", array("required"=>false))
                ->add("contact_email", "text", array("required"=>false))
                ->add("billing_address", "textarea", array("required"=>false))
                ->add("mailing_address", "textarea", array("required"=>false))
                ->add("miscellaneous", "textarea", array("required"=>false));

//        $builder->add("projects", "collection", array("type" => new ProjectType(), "allow_add"=>true, "prototype"=>true));

    }

    public function getName() {
        return "organization";
    }

    public function getDefaultOptions(array $options) {
        return array(
                'data_class' => 'Monistix\OrganizationBundle\Entity\Organization',
                );
    }
}
