package org.peter.domain.article.b;

import org.peter.domain.article.d.entities.Article;

public interface IArticleServices {

    public Article saveArticle(Article article);
    
    public Article findArticle(Long id);
    /*
    public void deleteArticle(Long id);
    */
}
