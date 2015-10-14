# -*- coding: utf-8 -*-
import werkzeug
import mimetypes

from openerp import http

from openerp.addons.web import http
from openerp.addons.web.http import request
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from openerp import tools

class KderpWebsite(http.Controller):
    #some variables
    qa_blog = 'Quality Safety Assurance'
    news_blog = 'General News'
    work_blog = 'Major Works'
    it_blog = 'IT'
    kdvn_route = '/kdvn'
    _post_per_page = 8
    #Them bien 
    es_blog = 'Electrical Systems'
    ms_blog = 'Mechanical Systems'
    kinqnews = 'KinQ News'
    kinvqnews = 'KinVQ News'
        
    def kdvn_posts(self, blog_name_list=[], tag_name_list=[], post_ids=[], page_url='/', page=1, template=['kderp_website.page_show_post', 'kderp_website.page_list_posts']):
        """Getting all posts of blog(s) to prepare to show
        - If only 1 post return, show the post
        - If more than 1 post return, list these posts
            + Handle pager
            + TODO: Handle and condition for tag
        """
        #Dinh dang ngay thang trong odoo
        def sd(date):
            return date.strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)
        today = datetime.today()
        
        announcements = http.request.env['blog.post'].search([('blog_id', '=', 'Announcement'), ("create_date", ">=", sd(today - relativedelta(days=7)))])
        funfacts = http.request.env['blog.post'].search([('blog_id','=','Fun Fact')])
        events = http.request.env['event.event'].search([("date_begin", ">=", sd(today))], limit=6)
        #dat bien all_posts de su dung chung trong nhieu truong hop
        all_posts = http.request.env['blog.post']
        if post_ids:
            search_domain = [('id', 'in', post_ids)]
        else:
            if blog_name_list:
                search_domain = [('blog_id', 'in', blog_name_list)]
            if tag_name_list:
                #do blog.tag va blog.post link voi nhau thong qua truong tag_ids 
                #la truong many2many, nen tam thoi duyet tags truoc
                #sau do join cac recordsets tra ve tu blog.tag de lay post_ids
                tags = http.request.env['blog.tag'].search([('name', 'in', tag_name_list)])
                #sudung map va reduce de lay join recordset cua post tra ve tu blog.tag
                #luu y ban than odoo co bo sung mapped va filltered cho recordset
                post_ids = tags.mapped('post_ids').mapped('id')
                #tags_posts = map(lambda tag: tag.post_ids, tags)
                #taged_posts = reduce(lambda a, c: a | c, tags_posts)
                #post_ids = taged_posts.mapped('id')
                search_domain.append(('id', 'in', post_ids))
        
        result = http.request.env['blog.post'].search(search_domain)
        if len(result) == 1:
            # Return only one post
            return http.request.render(template[0],{'post':result,'announcements': announcements,'ffacts': funfacts,'events':events})
        elif len(result) > 1:
            # Return posts -> list posts
            # Handler pager
            pager = request.website.pager(
                url = page_url,
                page = page,
                total = len(result),
                step = self._post_per_page
            )
            #limit and offset result
            result = http.request.env['blog.post'].search(search_domain, offset=(page-1)*self._post_per_page, limit=self._post_per_page)
            return http.request.render(template[1],{
                'posts': result,
                'pager': pager,
                'announcements': announcements,
                'ffacts': funfacts
            })
            
    
    @http.route('/intro/kdvn/<intro_name>', auth='public', website=True)
    def aboutus(self,intro_name):
        intro_dic = {
            'aboutus': 47,
            'aircon': 50,
            'electricalsystems': 48,
            'housing': 49,
            'environment': 51,
            'what_is_qa':53
            }
        return self.kdvn_posts(post_ids=[intro_dic[intro_name]],template=['kderp_website.intro', 'kderp_website.intro'])
    
    @http.route('/intro/termofuse', auth='public', website=True)
    def termofuse(self):
        return self.kdvn_posts(post_ids=[34])
    
    @http.route('/intro/contactus', auth='public', website=True)
    def contacts(self, **kw):
        """Showing all KDVN contacts: offices and site offices"""
        
        offices = http.request.env['res.partner'].search([('category_id.name','=','KDVN_Office')])
        sites = http.request.env['res.partner'].search([('category_id.name','=','KDVN_Site_Office')])
        return http.request.render('kderp_website.contacts',{
            'offices': offices,
            'sites': sites
        })
        
    @http.route(['/<submenu>/news', '/<submenu>/news/page/<int:page>','/<submenu>/tag/<subtag>','/<submenu>/tag/<subtag>/page/<int:page>'], auth='public', website=True)
    def kdvn_list_posts(self, page=1, submenu='intro', subtag='all'):
        """Showing KDVN News, blog based on route header"""
        
        submenu_dic = {
            'intro':[self.news_blog, self.qa_blog, self.it_blog, self.es_blog, self.ms_blog],
            'qa':[self.qa_blog],
            'it':[self.it_blog],
            #them submenu
            'es':[self.es_blog],
            'ms':[self.ms_blog]          
            }
        sub_tag = {
            'all': [],
            'kinqnews':[self.kinqnews],
            'kinvqnews': [self.kinvqnews]
                   }
        if (subtag == 'all'):
            url = '/' + submenu + '/news'
        else:
            url ='/' + submenu + '/tag/' + subtag
        return self.kdvn_posts(submenu_dic[submenu], sub_tag[subtag], [], url, page)
        #Works = self.kdvn_posts([work_blog])
        
    @http.route(['/<submenu>/news/<model("blog.post"):post>','/<submenu>/news/page/<int:page>/<model("blog.post"):post>','/<submenu>/tag/<subtag>/<model("blog.post"):post>','/<submenu>/tag/<subtag>/page/<int:page>/<model("blog.post"):post>'], auth='public', website=True)
    def kdvn_show_post(self, post, submenu, subtag='', page=1):
        """Showing post content"""
        return self.kdvn_posts([],[], [post.id])

    @http.route('/intro' + '/<model("blog.post"):post>', auth='public', website=True)
    def kdvn_show_intro(self, post):
        """Showing intro post content"""
        return self.kdvn_posts([], [post.id], template=['kderp_website.intro', 'kderp_website.intro'])
        
    @http.route(kdvn_route + '/qa_news/<model("blog.post"):post>', auth='public', website=True)
    def kdvn_show_qa_post(self, post):
        """Showing qa post content"""
        return self.kdvn_posts([], [post.id])
        
    @http.route('/blog/<blog>', auth='public', website=True)
    def kdvn_list_blog(self, blog):
        return self.kdvn_posts(blog_name_list=[blog])

    @http.route(['/intro/kdvn/what_is_qa', '/qa/what_is_qa'], auth="public", website=True)
    def kdvn_about_qa(self):
        return self.kdvn_posts([], post_ids=[53],template=['kderp_website.intro', 'kderp_website.intro'])
    
    @http.route('/website/image/<model>/<id>/<field>/<name>', auth='public', website=True)
    def kdvn_show_attach_file(self, model, id, field, name):
        """
        Return raw data of attachment as well as trying to guest
        mimetype of the attachment: mostly being used for showing pdf file
        TODO: this just temporary solved pdf file, there will be more cases have to take care of
        """
        response = werkzeug.wrappers.Response()
        
        #image = Image.open(cStringIO.StringIO(data))
        #response.mimetype = Image.MIME[image.format]

        #filename = '%s_%s.%s' % (model.replace('.', '_'), id, str(image.format).lower())
        #response.headers['Content-Disposition'] = 'inline; filename="%s"' % filename
        data = http.request.env['ir.attachment'].search([('id','=',id.split('_')[0])])
        response.data = data[field].decode('base64')
        file_ext = data.name[-4:]
        response.mimetype= mimetypes.types_map[file_ext]
        
        return response
    
    def kdvn_file_library(self, post_id, page, pager_url, template='kderp_website.files'):
        """
        Handling posts that manage attachments as media:
        - Images
        - Attached Files
        - Video
        """
        post = http.request.env['blog.post'].search([('id','=', post_id)])
        file_ids = post.img_url_ids
        files = file_ids[(page-1)*self._post_per_page:page*self._post_per_page]
        
        pager = request.website.pager(
                url = pager_url,
                page = page,
                total = len(file_ids),
                step = self._post_per_page                      
                )
        return http.request.render(template, {
            'files': files,
            'pager': pager,
            'post': post                                  
            })
    
    @http.route(['/kdvn/images',
                 '/kdvn/images/page/<int:page>'], website=True)
    def kdvn_image_library(self, page=1):
        """
        Keep KINDEN VIETNAM images
        """
        
        return self.kdvn_file_library(44, page, '/kdvn/images', 'kderp_website.files')
    
    @http.route(['/it/download', '/it/download/page/<int:page>', '/it/files', '/it/files/page/<int:page>'], auth='public', website=True)
    def kdvn_download(self, page=1):
        return self.kdvn_file_library(46, page, '/kdvn/download')
    
    @http.route('/intro/jobs', auth='public', website=True)
    def kdvn_job(self):
        return http.request.render('kderp_website.page_job')
    
    @http.route(['/intro/testimonials', '/intro/testimonials/<int:cur_index>'], auth="public", website=True)
    def kdvn_testi(self, cur_index=0):
        """Showing testimonials with next and previous button"""
        posts = http.request.env['blog.post'].search([('blog_id', '=', 'Testimonial')])
            
        if cur_index == 0:
            pre_index = len(posts) - 1
        else:
            pre_index = cur_index -1
            
        next_index = (cur_index + 1) % len(posts)
        
        return http.request.render('kderp_website.page_testi', {
            'index': [pre_index, cur_index, next_index],
            'post': posts[cur_index],
            'posts':posts                                                    
            })
