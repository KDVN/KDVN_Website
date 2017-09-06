# -*- coding: utf-8 -*-
import base64

import werkzeug
import werkzeug.urls

import mimetypes
from openerp import http, SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from openerp import tools

from openerp.addons.website_crm.controllers.main import contactus

class KderpWebsite(http.Controller):
  # some variables
  qa_blog = 'Quality Safety Assurance'
  qa_internal_tags =['KinQ News', 'KinVQ News']
  news_blog = 'General News'
  work_blog = 'Major Works'
  it_blog = 'IT'
  kdvn_route = '/kdvn'
  _post_per_page = 8
  # Them bien
  es_blog = 'Electrical Systems'
  ms_blog = 'Mechanical Systems'
  kinqnews = 'KinQ News'
  kinvqnews = 'KinVQ News'
  es_main = 'Electrical Maintenance'

  def kdvn_posts(self, blog_name_list=[], tag_name_list=[], post_ids=[], page_url='/', page=1,
                 template=['kderp_website.page_show_post', 'kderp_website.page_list_posts'], other_domain_search=[], **kwargs):
    """
    Getting all posts of blog(s) to prepare to show
        - If only 1 post return, show the post
        - If more than 1 post return, list these posts
        - Using other_domain_search for special search for example tag_ids.name
    """
    def _tag_search(search_domain):
      """
      blog.tag la truong many2many nen khi search voi dieu kien NOT
      ket qua tra ve se khong dung nhu mong muon. Method nay xu ly dieu kien
      search cua tag
      :return: search_domain
      """
      not_in_tags_search = filter(lambda s: s[0] == 'tag_ids.name' and s[1] == 'not in', search_domain)
      #not_in_tags_search.insert(0, '!')
      if not_in_tags_search:
        search_domain.remove(not_in_tags_search[0])
        post_ids_tags_search = http.request.env['blog.post'].search(['!', not_in_tags_search[0]]).mapped('id')
        search_domain.append(('id', 'not in', post_ids_tags_search))
      return search_domain

    def sd(date):
      """
       Dinh dang ngay thang theo odoo server settings
      :return: dd-mm-yyyy
      """
      return date.strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)

    today = datetime.today()
    
    #Cac announcement duoc hien thi trong bao nhieu ngay do relative_date
    #vi du relative_date = 7 thi announcement chi hien thi trong 7 ngay tinh tu ngay tao create_date 
    env = request.env(context=dict(request.env.context))
    Posts = env['blog.post']
    announcement_ids = Posts.search([('blog_id', '=', 'Announcement')]).ids
    announcements = Posts.sudo().browse(announcement_ids)
    announcements = set(j for j in announcements if j.create_date >= sd(today - relativedelta(days=j.relative_date)))
    ####################
    
    funfacts = http.request.env['blog.post'].search([('blog_id', '=', 'Fun Fact')])
    events = http.request.env['event.event'].search([("date_begin", ">=", sd(today))], limit=6)

    if post_ids:
      search_domain = [('id', 'in', post_ids)]
    else:
      if blog_name_list:
        search_domain = [('blog_id', 'in', blog_name_list)]
        if tag_name_list:
          search_domain.append(('tag_ids.name', 'in', tag_name_list))
    #handle for not in tags search
    other_domain_search = _tag_search(other_domain_search)
    search_domain += other_domain_search

    result = http.request.env['blog.post'].search(search_domain, order="priority desc", **kwargs)
    if len(result) == 1:
      # Return only one post
      return http.request.render(template[0],
                                 {'post': result, 'announcements': announcements, 'ffacts': funfacts, 'events': events})
    elif len(result) > 1:
      # Return posts -> list posts
      # Handler pager
      pager = request.website.pager(
        url=page_url,
        page=page,
        total=len(result),
        step=self._post_per_page
      )
      # limit and offset result
      result = http.request.env['blog.post'].search(search_domain, order="priority desc", offset=(page - 1) * self._post_per_page,
                                                    limit=self._post_per_page)
      return http.request.render(template[1], {
        'posts': result,
        'pager': pager,
        'announcements': announcements,
        'ffacts': funfacts
      })

  @http.route('/intro/kdvn/<intro_name>', auth='public', website=True)
  def aboutus(self, intro_name):
    intro_dic = {
      'aboutus': 47,
      'aircon': 50,
      'electricalsystems': 48,
      'housing': 49,
      'environment': 134,
      'what_is_qa': 53
    }
    return self.kdvn_posts(post_ids=[intro_dic[intro_name]], template=['kderp_website.intro', 'kderp_website.intro'])

  @http.route('/intro/termofuse', auth='public', website=True)
  def termofuse(self):
    return self.kdvn_posts(post_ids=[34])

  @http.route('/intro/contactus', auth='public', website=True)
  def contacts(self, **kw):
    """Showing all KDVN contacts: offices and site offices"""

    offices = http.request.env['res.partner'].search([('category_id.name', '=', 'KDVN_Office')])
    sites = http.request.env['res.partner'].search([('category_id.name', '=', 'KDVN_Site_Office')])
    return http.request.render('kderp_website.contacts', {
      'offices': offices,
      'sites': sites
    })

  @http.route(['/<submenu>/news', '/<submenu>/news/page/<int:page>', '/<submenu>/tag/<subtag>',
               '/<submenu>/tag/<subtag>/page/<int:page>'], auth='public', website=True)
  def kdvn_list_posts_public(self, page=1, submenu='intro', subtag='all'):
    """Showing KDVN News, blog based on route header on public pages"""
    submenu_dic = {
      # submenu or blog category
      'intro': [self.news_blog, self.qa_blog, self.it_blog, self.es_blog, self.ms_blog],
      'qa': [self.qa_blog],
      'it': [self.it_blog],
      'es': [self.es_blog],
      'ms': [self.ms_blog],
      'ba': [self.es_blog, self.ms_blog]
    }
    subtag_dic = {
      'all': [],
      'es_main': [self.es_main]
    }
    if submenu not in submenu_dic.keys():
      submenu = 'intro'
    if subtag not in subtag_dic.keys():
      subtag = 'all'
    if subtag == 'all':
      url = '/' + submenu + '/news'
    else:
      url = '/' + submenu + '/tag/' + subtag
    return self.kdvn_posts(submenu_dic[submenu], subtag_dic[subtag], [], url, page, other_domain_search=[('tag_ids.name', 'not in', self.qa_internal_tags)])

  @http.route(['/qa/tag/<subtag>', '/qa/tag/<subtag>/page/<int:page>'], auth='user', website=True)
  def kdvn_list_posts_internal(self, page=1, submenu='intro', subtag='all'):
    """Showing KDVN News, blog based on route header"""
    subtag_dic = {
      'all': [],
      'kinqnews': [self.kinqnews],
      'kinvqnews': [self.kinvqnews],
    }
    if subtag not in subtag_dic.keys():
      subtag = 'all'
    url = '/' + submenu + '/tag/' + subtag
    return self.kdvn_posts([self.qa_blog], subtag_dic[subtag], [], url, page)

  @http.route(['/<submenu>/news/<model("blog.post"):post>', '/<submenu>/news/page/<int:page>/<model("blog.post"):post>'], auth='public', website=True)
  def kdvn_show_post_public(self, post, submenu, subtag='', page=1):
    """Showing post content"""
    #Loc du lieu QSA chi hien thi khi dang nhap
    #Neu la publish user thi khong hien thi noi dung QSA
    if request.uid == request.website.user_id.id:
      return self.kdvn_posts([], [], [post.id], other_domain_search=[('tag_ids.name', 'not in', self.qa_internal_tags), ('blog_id', '!=', 'Quality Safety Assurance')])
    else:
      # Neu la login user thi hien thi noi dung cac QSA ma khong co trong tags
      return self.kdvn_posts([], [], [post.id], other_domain_search=[('tag_ids.name', 'not in', self.qa_internal_tags)])

  # Chi hien thi chi tiet QSA khi dang nhap
  @http.route(['/qa/news/<model("blog.post"):post>', '/qa/news/page/<int:page>/<model("blog.post"):post>'], auth='user', website=True)
  def kdvn_show_post_qa(self, post, submenu='', subtag='', page=1):
    """Showing post content"""
    return self.kdvn_posts([], [], [post.id])

  @http.route(['/qa/news', '/qa/news/page/<int:page>'], auth='user', website=True)
  def kdvn_list_posts_qa(self, page=1, submenu='', subtag=''):
    return self.kdvn_posts([self.qa_blog], [], [], '/qa/news', page)

  @http.route(['/<submenu>/tag/<subtag>/<model("blog.post"):post>', '/<submenu>/tag/<subtag>/page/<int:page>/<model("blog.post"):post>'], auth='user', website=True)
  def kdvn_show_post_internal(self, post, submenu, subtag='', page=1):
    """Showing post content"""
    return self.kdvn_posts([], [], [post.id])

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
    return self.kdvn_posts([], post_ids=[53], template=['kderp_website.intro', 'kderp_website.intro'])

  @http.route('/website/image/<model>/<id>/<field>/<name>', auth='public', website=True)
  def kdvn_show_attach_file(self, model, id, field, name):
    """
        Return raw data of attachment as well as trying to guest
        mimetype of the attachment: mostly being used for showing pdf file
        TODO: this just temporary solved pdf file, there will be more cases have to take care of
        """
    response = werkzeug.wrappers.Response()

    # image = Image.open(cStringIO.StringIO(data))
    # response.mimetype = Image.MIME[image.format]

    # filename = '%s_%s.%s' % (model.replace('.', '_'), id, str(image.format).lower())
    # response.headers['Content-Disposition'] = 'inline; filename="%s"' % filename
    data = http.request.env['ir.attachment'].search([('id', '=', id.split('_')[0])])
    response.data = data[field].decode('base64')
    file_ext = data.name[-4:]
    response.mimetype = mimetypes.types_map[file_ext]

    return response

  def kdvn_file_library(self, post_id, page, pager_url, template=['kderp_website.files', 'website.homepage']):
    """
        Handling posts that manage attachments as media:
        - Images
        - Attached Files
        - Video
        """
    post = http.request.env['blog.post'].search([('id', '=', post_id)])
    file_ids = post.img_url_ids
    files = file_ids[(page - 1) * self._post_per_page:page * self._post_per_page]

    pager = request.website.pager(
      url=pager_url,
      page=page,
      total=len(file_ids),
      step=self._post_per_page
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

  @http.route(['/it/download', '/it/download/page/<int:page>', '/it/files', '/it/files/page/<int:page>',
               '/intro/download', '/intro/download/page/<int:page>', '/intro/files', '/intro/files/page/<int:page>'
               ], auth='public',
              website=True)
  def kdvn_download(self, page=1):
    return self.kdvn_file_library(46, page, '/kdvn/download')

  @http.route('/intro/jobs', auth='public', website=True)
  def kdvn_job(self):
    posts = http.request.env['blog.post'].search([('blog_id', '=', 'Jobs')])
    return http.request.render('kderp_website.page_job', {'posts': posts})
  #
  # @http.route(['/intro/testimonials', '/intro/testimonials/<int:cur_index>'], auth="public", website=True)
  # def kdvn_testi(self, cur_index=0):
  #   """Showing testimonials with next and previous button"""
  #   posts = http.request.env['blog.post'].search([('blog_id', '=', 'Testimonial')])
  #
  #   if cur_index == 0:
  #     pre_index = len(posts) - 1
  #   else:
  #     pre_index = cur_index - 1
  #
  #   next_index = (cur_index + 1) % len(posts)
  #
  #   return http.request.render('kderp_website.page_testi', {
  #     'index': [pre_index, cur_index, next_index],
  #     'post': posts[cur_index],
  #     'posts': posts
  #   })

  @http.route(['/intro/certificates', '/intro/certificates/<int:cur_index>'], auth="public", website=True)
  def kdvn_testi(self, cur_index=0):
    """Showing testimonials with next and previous button"""
    posts = http.request.env['blog.post'].search([('blog_id', '=', 'Certificates')], order="priority desc")

    if cur_index == 0:
      pre_index = len(posts) - 1
    else:
      pre_index = cur_index - 1

    next_index = (cur_index + 1) % len(posts)

    return http.request.render('kderp_website.page_certificates', {
      'index': [pre_index, cur_index, next_index],
      'post': posts[cur_index],
      'posts': posts
    })
    
  #@http.route('/crm/contactus', auth="public")
  
class Kdvn_contactus(contactus):
  """
  Inherited website_crm to enable upload multiple file attachments
  TODO: DRY; only pdf and image; size; number of files
  """

  @http.route()
  # Original route: /crm/contactus
  def contactus(self, **kwargs):
    def dict_to_str(title, dictvar):
            ret = "\n\n%s" % title
            for field in dictvar:
                ret += "\n%s" % field
            return ret

    _MAX_SIZE = 2 * 1024 * 1024 #2MB
    _TECHNICAL = ['show_info', 'view_from', 'view_callback']  # Only use for behavior, don't stock it
    _BLACKLIST = ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'user_id', 'active']  # Allow in description
    _REQUIRED = ['name', 'contact_name', 'email_from', 'description']  # Could be improved including required from model

    post_file = []  # List of file to add to ir_attachment once we have the ID
    post_description = []  # Info to add after the message
    values = {}

    values['medium_id'] = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'crm.crm_medium_website')
    values['section_id'] = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'website.salesteam_website_sales')

    for field_name, field_value in kwargs.items():
        if hasattr(field_value, 'filename'):
            #post_file.append(field_value)
            post_file.extend(http.request.httprequest.files.getlist('filename'))
        elif field_name in request.registry['crm.lead']._fields and field_name not in _BLACKLIST:
            values[field_name] = field_value
        elif field_name not in _TECHNICAL:  # allow to add some free fields or blacklisted field like ID
            post_description.append("%s: %s" % (field_name, field_value))

    if "name" not in kwargs and values.get("contact_name"):  # if kwarg.name is empty, it's an error, we cannot copy the contact_name
        values["name"] = values.get("contact_name")
    # fields validation : Check that required field from model crm_lead exists
    error = set(field for field in _REQUIRED if not values.get(field))

    if error:
        values = dict(values, error=error, kwargs=kwargs.items())
        return request.website.render(kwargs.get("view_from", "website.contactus"), values)

    # description is required, so it is always already initialized
    if post_description:
        values['description'] += dict_to_str(_("Custom Fields: "), post_description)

    if kwargs.get("show_info"):
        post_description = []
        environ = request.httprequest.headers.environ
        post_description.append("%s: %s" % ("IP", environ.get("REMOTE_ADDR")))
        post_description.append("%s: %s" % ("USER_AGENT", environ.get("HTTP_USER_AGENT")))
        post_description.append("%s: %s" % ("ACCEPT_LANGUAGE", environ.get("HTTP_ACCEPT_LANGUAGE")))
        post_description.append("%s: %s" % ("REFERER", environ.get("HTTP_REFERER")))
        values['description'] += dict_to_str(_("Environ Fields: "), post_description)

    lead_id = self.create_lead(request, dict(values, user_id=False), kwargs)
    values.update(lead_id=lead_id)
    if lead_id:
        for field_value in post_file:
            #TODO: users can easily change files extension
            #TODO: limit number of files upload
            if (field_value.mimetype in ['application/pdf','image/jpeg']):
              #Check file size. TODO: Client side?
              blob = field_value.read()
              if len(blob) <= _MAX_SIZE:
                attachment_value = {
                    'name': field_value.filename,
                    'res_name': field_value.filename,
                    'res_model': 'crm.lead',
                    'res_id': lead_id,
                    'datas': base64.encodestring(blob),
                    'datas_fname': field_value.filename,
                }
                request.registry['ir.attachment'].create(request.cr, SUPERUSER_ID, attachment_value, context=request.context)

    return self.get_contactus_response(values, kwargs)
  