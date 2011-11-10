<?php

namespace Monistix\OrganizationBundle\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilder;

class ProjectType extends AbstractType {

    public function buildForm(FormBuilder $builder, array $options) {

        $builder->add('name', 'text')
                ->add('active', 'checkbox')
                ->add('contact_name', 'text', array("required"=>false))
                ->add('contact_number', 'text', array("required"=>false))
                ->add('contact_email', 'text', array("required"=>false))
                ->add('miscellaneous', 'textarea', array("required"=>false));

    }

    public function getName() {
        return 'project';
    }

    public function getDefaultOptions(array $options) {
        return array(
                'data_class' => 'Monistix\OrganizationBundle\Entity\Project',
                );
    }
}
