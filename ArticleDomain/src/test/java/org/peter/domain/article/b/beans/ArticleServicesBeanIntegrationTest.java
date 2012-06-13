package org.peter.domain.article.b.beans;

import static org.junit.Assert.*;

import javax.inject.Inject;

import org.dbunit.dataset.IDataSet;
import org.dbunit.operation.DatabaseOperation;
import org.junit.Before;
import org.junit.Test;
import org.peter.domain.article.b.IArticleServices;
import org.peter.domain.article.d.entities.Article;

import com.volvo.jvs.testsupport.dbunit.AbstractTransactionalDbUnitTestCase;


public class ArticleServicesBeanIntegrationTest extends AbstractTransactionalDbUnitTestCase {

    private String article_drop_ddl_file = "sql/article_drop_ddl.sql";
    private String article_create_ddl_file = "sql/article_create_ddl.sql";
    private String initialDataXmlFile = "data/initial.xml";
    
    @Inject
    private IArticleServices articleServices;
    
    @Before
    public void setUpTestData() throws Exception {
        executeSqlScript(article_drop_ddl_file, true);
        executeSqlScript(article_create_ddl_file, true);
        IDataSet dataSet = getDataSet(initialDataXmlFile);
        DatabaseOperation.CLEAN_INSERT.execute(getDbunitConnection(), dataSet);
    }
    
    @Test
    public void testSavingArticle(){
        Article article = new Article();
        article.setName("Peter");
        //insert
        
        articleServices.saveArticle(article);
        //check for id != 0
        assertEquals(1, article.getId());
    }
    
    
    @Test
    public void testFindCustomer() {
        Article article = articleServices.findArticle(-1001L);
        assertNotNull(article);
        assertEquals(-1001, article.getId());
    }
}
