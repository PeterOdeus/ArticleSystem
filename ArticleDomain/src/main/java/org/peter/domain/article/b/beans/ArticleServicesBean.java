package org.peter.domain.article.b.beans;

import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

import org.peter.domain.article.b.IArticleServices;
import org.peter.domain.article.d.entities.Article;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.volvo.jvs.runtime.platform.ContainerManaged;

@ContainerManaged
@TransactionAttribute(TransactionAttributeType.REQUIRED)
public class ArticleServicesBean implements IArticleServices{

    private static final Logger logger = LoggerFactory.getLogger(ArticleServicesBean.class);
    
    private EntityManager em = null;
    
    @PersistenceContext(unitName = "ArticlePU")
    public void setEntityManager(EntityManager em){
        this.em = em;
    }
    
    public EntityManager getEntityManager(){
        return this.em;
    }
    
    @Override
    public Article saveArticle(Article article) {
        if ( article.getId() == 0 ){
            logger.debug("Article Services --------- New Article");
            em.persist(article);
            return article;
        } else {
            logger.debug("Article Services --------- Update Article " + article);
            article = em.merge(article);
            logger.debug("Article Services --------- Update Article Done " + article);
            return article;
        }
    }

    @Override
    public Article findArticle(Long id) {
        Article article = em.find(Article.class, id);
        if ( article != null ) {
            logger.debug("Article Services --------- Article findArticle() article.id = " + article.getId());
        }
        return article;
    }
/*
    @Override
    public void deleteArticle(Long id) {
        Article article = em.find(Article.class, id);
        em.remove(article);
    }
*/
}
