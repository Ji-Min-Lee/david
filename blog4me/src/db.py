import redis


class DB:
    def __init__(self, logger):
        self.logger = logger
        self.conn = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    def add_category(self, name, p_cid):
        """
        Category: cid (int), name (string)
        Structure: id, p_cid, c_cid
        :return:
        """
        # category id를 얻음
        cid = self.conn.get("cid")
        self.conn.incr("cid")

        # category 정보 set
        self.conn.hset(f"category:{cid}", "name", name)
        self.conn.hset(f"category:{cid}", "parent", p_cid)
        self.conn.hset(f"category:{cid}", "children", "")
        self.conn.hset(f"category:{cid}", "content", "")

        # 부모 category의 children에 추가
        p_children = self.conn.hget(f"category:{p_cid}", "children")
        self.conn.hset(f"category:{cid}", "children", p_children + " " + cid)

        # logging
        self.logger.info(f"Category '{name}:{cid}' is successfully added")
        name = self.conn.hget(f"category:{cid}", "name")
        parent = self.conn.hget(f"category:{cid}", "parent")
        children = self.conn.hget(f"category:{cid}", "children")
        content = self.conn.hget(f"category:{cid}", "content")
        self.logger.info(f"name: {name}")
        self.logger.info(f"parent: {parent}")
        self.logger.info(f"children: {children}")
        self.logger.info(f"content: {content}")
        return cid

    def delete_category(self, cid):
        """
        Category, Structure에서 recursive하게 삭제해야 자손 카테고리가지 다 삭제 가능함

        삭제된 카테고리의 페이지도 삭제 필요
        :return:
        """

        p_cid = self.conn.hget(f"category:{cid}", "parent")
        p_children = self.conn.hget(f"category:{p_cid}", "children")
        p_children = p_children.split()
        p_children.remove(cid)
        self.conn.hset(f"category:{p_cid}", "children", " ".join(p_children))

        children = self.conn.hget(f"category:{cid}", "children")
        children = children.split()

        pages = self.conn.hget(f"category:{cid}", "content")
        pages = pages.split()

        self.conn.hdel(f"category:{cid}", "name")
        self.conn.hdel(f"category:{cid}", "parent")
        self.conn.hdel(f"category:{cid}", "children")
        self.conn.hdel(f"category:{cid}", "content")

        for page in pages:
            self.delete_page(page)

        for child in children:
            self.delete_category(child)

        # logging
        name = self.conn.hget(f"category:{cid}", "name")
        parent = self.conn.hget(f"category:{cid}", "parent")
        children = self.conn.hget(f"category:{cid}", "children")
        content = self.conn.hget(f"category:{cid}", "content")
        self.logger.info(f"Category '{name}:{cid}' is successfully removed")
        self.logger.info(f"name: {name}")
        self.logger.info(f"parent: {parent}")
        self.logger.info(f"children: {children}")
        self.logger.info(f"content: {content}")

    def add_page(self, cid, title, md_path):
        """
        Page: pid, title, md file path
        Content: cid, pid
        :return:
        """
        pid = self.conn.get("pid")
        self.conn.incr("pid")
        self.conn.hset(f"page:{pid}", "title", title)
        self.conn.hset(f"page:{pid}", "category", cid)
        self.conn.hset(f"page:{pid}", "md_path", md_path)
        pages = self.conn.hget(f"category:{cid}", "content")
        self.conn.hset(f"category:{cid}", "content", pages + " " + pid)

        # logging
        title = self.conn.hget(f"page:{cid}", "title")
        cid = self.conn.hget(f"page:{cid}", "category")
        md_path = self.conn.hget(f"page:{cid}", "md_path")
        self.logger.info(f"Page '{title}:{pid}' is successfully added")
        self.logger.info(f"title: {title}")
        self.logger.info(f"parent: {cid}")
        self.logger.info(f"md_path: {md_path}")
        pages = self.conn.hget(f"category:{cid}", "content")
        self.logger.info(f"page is in Category {cid}: {pages}")

    def delete_page(self, pid):
        self.conn.delete(f"page:{pid}")
        cid = self.conn.hget(f"page:{pid}", "category")
        pages = self.conn.hget(f"category:{cid}", "content")
        pages = pages.split()
        if pid in pages:
            pages.remove(pid)
        self.conn.hset(f"category:{cid}", "content", " ".join(pages))

        # logging
        title = self.conn.hget(f"page:{cid}", "title")
        cid = self.conn.hget(f"page:{cid}", "category")
        md_path = self.conn.hget(f"page:{cid}", "md_path")
        self.logger.info(f"Page '{title}:{pid}' is successfully removed")
        self.logger.info(f"title: {title}")
        self.logger.info(f"parent: {cid}")
        self.logger.info(f"md_path: {md_path}")
        pages = self.conn.hget(f"category:{cid}", "content")
        self.logger.info(f"page is not in Category {cid}: {pages}")
