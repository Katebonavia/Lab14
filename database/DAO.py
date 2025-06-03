from database.DB_connect import DBConnect
from model.edge import Edge
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        query = """select *
                    from stores s"""

        results = []

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(storeId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from orders o 
                    where o.store_id = %s"""

        results = []

        cursor.execute(query, (storeId,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(storeId, idMapNodes, K):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select o2.order_id as v1 , o1.order_id as v2, sum(oi2.quantity+oi1.quantity) as peso
                    from orders o1, orders o2, order_items oi1, order_items oi2
                    where o2.store_id = %s
                    and o1.store_id = %s
                    and o1.order_id < o2.order_id
                    and oi1.order_id = o1.order_id 
                    and oi2.order_id = o2.order_id 
                    and datediff( o2.order_date, o1.order_date)<%s
                    and abs(datediff( o2.order_date, o1.order_date))>0
                    group by o2.order_id , o1.order_id """

        results = []

        cursor.execute(query, (storeId,storeId, K))

        for row in cursor:
            results.append(Edge(idMapNodes[row['v1']], idMapNodes[row['v2']], row['peso']))

        cursor.close()
        conn.close()
        return results