import time
import random

class Node:
    all_instances= []
    def __init__(self, id):
        Node.all_instances.append(self)
        self.id = id
        self.parent = None
        self.children = []
        self.is_malicious = False
        self.messages_received= 0
        self.messages_sent= 0
        self.messages_generated= 0
        
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        
    
class DODAG:
    def __init__(self, root_id):
        self.nodes = {}
        self.root_id = root_id
        self.root = Node(root_id)
        self.nodes[root_id] = self.root
        self.total_messages_received = 0
        
    def add_node(self, id, parent_id):
        if id in self.nodes:
            return
        node = Node(id)
        self.nodes[id] = node
        parent = self.nodes[parent_id]
        parent.add_child(node)
        
    def generate_messages(self, num_messages):
        nodes = list(self.nodes.values())
        sources = [n for n in nodes if n != self.root]
        for i in range(num_messages):
            source = random.choice(sources)
            source.messages_generated+= 1
            message = {'source': source.id, 'seq_num': i}
            self.deliver_message(message)
            time.sleep(0.001)
            
    def deliver_message(self, message):
        node = self.nodes[message['source']]
        while node != self.root:
            if node.is_malicious:
                if random.random() <= 0.3:
                    return  # drop message
            node.messages_sent+= 1
            node = node.parent
            node.messages_received+= 1
        self.total_messages_received += 1
        print(f"Message {message['seq_num']} delivered to root node")
        
    def add_nodes(self, num_nodes):
        for i in range(2, num_nodes + 1):
            parent_id = random.randint(1, i-1)
            self.add_node(i, parent_id)

if __name__ == '__main__':
    dodag = DODAG(1)
    f = open("sfadodag100.txt", "w")
    total_nodes=int(input("Enter no of nodes : "))
    f.writelines("Total number of nodes : " + str(total_nodes)+'\n')
    dodag.add_nodes(total_nodes)
    number_of_malicious_nodes= int(input("Enter number of malicious nodes : "))
    for i in range(number_of_malicious_nodes):
        a=int(input("Enter id of malicious nodes : ")) 
        dodag.nodes[a].is_malicious = True
    total_messages=int(input("Enter no of messages : "))
    f.writelines("Total number of packets generated: " + str(total_messages)+'\n')
    f.writelines("\n")

    dodag.generate_messages(total_messages)
    for obj in Node.all_instances:
        sent=str(obj.messages_sent)
        received=str(obj.messages_received)
        node=str(obj.id)
        generated=str(obj.messages_generated)
        f.writelines( "Node " + node + " generated packets = "+ generated +"\n")
        f.writelines( "Node " + node + " received packets = "+ received+"\n")
        f.writelines( "Node " + node + " sent packets = "+sent+"\n")
        f.writelines("\n")
    for obj in Node.all_instances:
        sent=str(obj.messages_sent)
        received=str(obj.messages_received)
        node=str(obj.id)
        generated=str(obj.messages_generated)
        dropped= obj.messages_received + obj.messages_generated - obj.messages_sent
        dropping_prob=  ((dropped)/(obj.messages_received + obj.messages_generated))*100
        if dropped and obj.id!=1> 0:
            f.writelines("Node " + node + " is malicious with packet dropping ratio of " + str(dropping_prob) + "%"+"\n")
    f.writelines("\n")
    f.writelines("Total number of packets delivered to root node : " + str(dodag.total_messages_received)+'\n')
    overall_delivery_ratio=(dodag.total_messages_received/total_messages)*100
    f.writelines("Overall_delivery_ratio is : " + str(overall_delivery_ratio) + "%"+'\n')
    f.writelines("Propagation delay is : " + str(1*total_messages)+"ms" +'\n')
    

# In this example, the DODAG class has been updated to include a generate_messages method 
# that generates a specified number of messages at random source nodes and delivers them to the root node.
# The deliver_message method simulates the delivery of a message by traversing the DODAG from 
# the source node to the root node and checking if any nodes along the way are malicious.
# If a malicious node is encountered, the message is dropped with a 30% probability.
# In this updated version, we keep track of the number of messages received by the root node 
# in a messages_received attribute of the DODAG class. This attribute is incremented each time
# a message is successfully delivered to the root node in the deliver_message method.
# The output of the program should now show the number of messages that were successfully delivered
# to the root node.