import redis


class Repository:
    def __init__(self):
        self.conn = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        # self.conn.set("cid", 0)
        # self.conn.hset(f"category:-1", "children", "")

    def add_category(self, name, parent_id):
        cid = self.conn.get("cid").decode("utf-8")
        self.conn.incr("cid")

        self.conn.hset(f"category:{cid}", "name", name)
        self.conn.hset(f"category:{cid}", "parent", parent_id)
        self.conn.hset(f"category:{cid}", "children", "")

        children = self.conn.hget(f"category:{parent_id}", "children")
        if children is None:
            children = ""
        else:
            children = children.decode("utf-8")
        children += " " + cid
        print(parent_id, children)
        self.conn.hset(f"category:{parent_id}", "children", children)
        return cid

    def delete_category(self, cid):
        parent_id = self.conn.hget(f"category:{cid}", "parent").decode("utf-8")

        self.conn.hdel(f"category:{cid}", "name")
        self.conn.hdel(f"category:{cid}", "parent")
        self.conn.hdel(f"category:{cid}", "children")

        parent_children = self.conn.hget(f"category:{parent_id}", "children").decode("utf-8")
        parent_children = parent_children.split()
        parent_children.remove(cid)
        self.conn.hset(f"category:{parent_id}", "children", " ".join(parent_children))

        self.delete_page(cid)

    def add_page(self, cid, md_path):
        self.conn.hset(f"page:{cid}", "md_path", md_path)

    def delete_page(self, cid):
        self.conn.hdel(f"page:{cid}", "md_path")

    def show_category(self, cid):
        name = self.conn.hget(f"category:{cid}", "name")
        parent_id = self.conn.hget(f"category:{cid}", "parent")
        children = self.conn.hget(f"category:{cid}", "children")
        print("== Show Category ==")
        print("cid: ", cid)
        print("name: ", name)
        print("parent_id: ", parent_id, self.get_name_by_cid(parent_id))
        if children is None:
            children = []
        else:
            children = children.decode("utf-8").split()
        for child in children:
            print("child: ", child, self.get_name_by_cid(child))
        if parent_id != -1:
            parent_children = self.conn.hget(f"category:{parent_id}", "children")
            print("parent_children: ", parent_children)
        md_path = self.conn.hget(f"page:{cid}", "md_path")
        print("md_path: ", md_path)

    def get_name_by_cid(self, cid):
        name = self.conn.hget(f"category:{cid}", "name")
        if name is None:
            return name
        return name.decode("utf-8")

    def get_children(self, cid):
        children = self.conn.hget(f"category:{cid}", "children").decode("utf-8")
        if children is not None:
            children = children.split()
        else:
            children = []
        children_dict = dict()
        for child in children:
            name = self.get_name_by_cid(child)
            children_dict[child.decode("utf-8")] = name
        return children_dict

    def get_parent(self, cid):
        parent_cid = self.conn.hget(f"category:{cid}", "parent").decode("utf-8")
        parent_name = self.get_name_by_cid(parent_cid)
        return parent_cid, parent_name


if __name__ == "__main__":
    repo = Repository()

    python_id = repo.add_category("Python", -1)
    aws_id = repo.add_category("AWS", -1)
    flask_id = repo.add_category("Flask", -1)

    devpi_id = repo.add_category("devpi", python_id)
    repo.add_page(devpi_id, "path_to_md")

    cognito_id = repo.add_category("Cognito", aws_id)
    lambda_id = repo.add_category("Lambda", aws_id)

    repo.show_category(python_id)
    repo.show_category(devpi_id)
    repo.show_category(aws_id)
