<?php

namespace Monistix\OrganizationBundle\Controller;

use Monistix\OrganizationBundle\Entity\Organization;
use Monistix\OrganizationBundle\Entity\Project;
use Monistix\OrganizationBundle\Form\OrganizationType;
use Monistix\OrganizationBundle\Form\ProjectType;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;

class DefaultController extends Controller {

	public function listAction() {

        $organizations = $this->get('doctrine')->getEntityManager()
                ->createQuery('SELECT o FROM MonistixOrganizationBundle:Organization o')
                ->execute();

		return $this->render('MonistixOrganizationBundle:Default:list.html.twig', array('organizations' => $organizations));

	}

	public function addAction(Request $request) {

		$form = $this->createForm(new OrganizationType(), new Organization());

        if ($request->getMethod() == 'POST') {

            $form->bindRequest($request);

            if ($form->isValid()) {

                $this->getDoctrine()->getEntityManager()
                     ->persist($form->getData())
                     ->flush();

                $this->get('session')->setFlash('notice', '<strong>'.$form->getData()->getName().'</strong> was successfully saved');
                return $this->redirect($this->generateUrl('list_organization'));

            }
        }

		return $this->render('MonistixOrganizationBundle:Default:form.html.twig', array(
					'form'=>$form->createView(),
					));
	}

	public function updateAction($id) {

        $organization = $this->getDoctrine()->getRepository('MonistixOrganizationBundle:Organization')->findOneById($id);

        if (!$organization) throw $this->createNotFoundException('The organization does not exist');

		$form = $this->createForm(new OrganizationType(), $organization);

        if ($this->get("request")->getMethod() == 'POST') {

            $form->bindRequest($this->get("request"));

            if ($form->isValid()) {

                $em = $this->getDoctrine()->getEntityManager();
                $em->persist($form->getData());
                $em->flush();

                $this->get('session')->setFlash('notice', '<strong>'.$form->getData()->getName().'</strong> was successfully saved');
                return $this->redirect($this->generateUrl('list_organization'));

            }
        }

		return $this->render('MonistixOrganizationBundle:Default:form.html.twig', array(
					'form'=>$form->createView(),
					));
	}

	public function deleteAction($id) {

        $organization = $this->getDoctrine()->getRepository('MonistixOrganizationBundle:Organization')->findOneById($id);

        if (!$organization) throw $this->createNotFoundException('The organization does not exist');
        $this->get("logger")->debug("potato");

        if ($this->get("request")->getMethod() == 'POST') {

            $em = $this->getDoctrine()->getEntityManager();
            $em->remove($organization);
            $em->flush();

        } 

        return new Response(json_encode(true));

	}
}
