
from sequence.qlan.qlan_orchestrator import QlanOrchestratorNode
from sequence.qlan.qlan_client import QlanClientNode
from sequence.kernel.timeline import Timeline
from sequence.components.optical_channel import ClassicalChannel
from sequence.qlan.qlan_measurement import QlanMeasurementMsgType, QlanB0MsgType

def pair_protocol(orchestrator: QlanOrchestratorNode, clients: list[QlanClientNode]):
    
    p_orch = orchestrator.protocols[0]
    orch_memo_name1 = orchestrator.resource_manager.memory_names[0]
    clients_names = []
    clients_memory_names = []
    
    for client in clients:
        clients_names.append(client.name)
        clients_memory_names.append(client.resource_manager.memory_names[0])

    p_orch.set_others([], clients_names, [orch_memo_name1])


def test_send_outcome_messages_z_0():
    tl = Timeline()

    test_client1 = QlanClientNode(name='test_client1',
                            tl=tl, 
                            num_local_memories=1)
    test_client2 = QlanClientNode(name='test_client2',
                            tl=tl, 
                            num_local_memories=1)
    
    test_memo1 = test_client1.get_components_by_type("Memory")[0]
    test_memo2 = test_client2.get_components_by_type("Memory")[0]

    test_orch = QlanOrchestratorNode("test_orch",
                                tl, 
                                num_local_memories=1, 
                                remote_memories=[test_memo1, test_memo2])
    test_orch.set_seed(2)
    test_orch.update_bases('z')
    
    cc_o_c1 = ClassicalChannel("cc_o_c1", tl, 10, 1e9)
    cc_o_c2 = ClassicalChannel("cc_o_c2", tl, 10, 1e9)
    cc_o_c1.set_ends(test_orch, test_client1.name)
    cc_o_c2.set_ends(test_orch, test_client2.name)

    test_orch.resource_manager.create_protocol()

    tl.init()

    pair_protocol(orchestrator=test_orch, clients=[test_client1, test_client2])

    test_orch.protocols[0].start(test_orch)

    for i in range(len(test_orch.protocols[0].sent_messages)):
        assert test_orch.protocols[0].sent_messages[i] is QlanMeasurementMsgType.Z_Outcome0 

def test_send_outcome_messages_z_1():
    tl = Timeline()

    test_client1 = QlanClientNode(name='test_client1',
                            tl=tl, 
                            num_local_memories=1)
    test_client2 = QlanClientNode(name='test_client2',
                            tl=tl, 
                            num_local_memories=1)
    
    test_memo1 = test_client1.get_components_by_type("Memory")[0]
    test_memo2 = test_client2.get_components_by_type("Memory")[0]

    test_orch = QlanOrchestratorNode("test_orch",
                                tl, 
                                num_local_memories=1, 
                                remote_memories=[test_memo1, test_memo2])
    test_orch.set_seed(0)
    test_orch.update_bases('z')
    
    cc_o_c1 = ClassicalChannel("cc_o_c1", tl, 10, 1e9)
    cc_o_c2 = ClassicalChannel("cc_o_c2", tl, 10, 1e9)
    cc_o_c1.set_ends(test_orch, test_client1.name)
    cc_o_c2.set_ends(test_orch, test_client2.name)

    test_orch.resource_manager.create_protocol()

    tl.init()

    pair_protocol(orchestrator=test_orch, clients=[test_client1, test_client2])

    test_orch.protocols[0].start(test_orch)

    for i in range(len(test_orch.protocols[0].sent_messages)):
        assert test_orch.protocols[0].sent_messages[i] is QlanMeasurementMsgType.Z_Outcome1 


def test_send_outcome_messages_y_0():
    tl = Timeline()

    test_client1 = QlanClientNode(name='test_client1',
                            tl=tl, 
                            num_local_memories=1)
    test_client2 = QlanClientNode(name='test_client2',
                            tl=tl, 
                            num_local_memories=1)
    
    test_memo1 = test_client1.get_components_by_type("Memory")[0]
    test_memo2 = test_client2.get_components_by_type("Memory")[0]

    test_orch = QlanOrchestratorNode("test_orch",
                                tl, 
                                num_local_memories=1, 
                                remote_memories=[test_memo1, test_memo2])
    test_orch.set_seed(2)
    test_orch.update_bases('y')
    
    cc_o_c1 = ClassicalChannel("cc_o_c1", tl, 10, 1e9)
    cc_o_c2 = ClassicalChannel("cc_o_c2", tl, 10, 1e9)
    cc_o_c1.set_ends(test_orch, test_client1.name)
    cc_o_c2.set_ends(test_orch, test_client2.name)

    test_orch.resource_manager.create_protocol()

    tl.init()

    pair_protocol(orchestrator=test_orch, clients=[test_client1, test_client2])

    test_orch.protocols[0].start(test_orch)

    for i in range(len(test_orch.protocols[0].sent_messages)):
        assert test_orch.protocols[0].sent_messages[i] is QlanMeasurementMsgType.Y_Outcome0 

def test_send_outcome_messages_y_1():
    tl = Timeline()

    test_client1 = QlanClientNode(name='test_client1',
                            tl=tl, 
                            num_local_memories=1)
    test_client2 = QlanClientNode(name='test_client2',
                            tl=tl, 
                            num_local_memories=1)
    
    test_memo1 = test_client1.get_components_by_type("Memory")[0]
    test_memo2 = test_client2.get_components_by_type("Memory")[0]

    test_orch = QlanOrchestratorNode("test_orch",
                                tl, 
                                num_local_memories=1, 
                                remote_memories=[test_memo1, test_memo2])
    test_orch.set_seed(0)
    test_orch.update_bases('y')
    
    cc_o_c1 = ClassicalChannel("cc_o_c1", tl, 10, 1e9)
    cc_o_c2 = ClassicalChannel("cc_o_c2", tl, 10, 1e9)
    cc_o_c1.set_ends(test_orch, test_client1.name)
    cc_o_c2.set_ends(test_orch, test_client2.name)

    test_orch.resource_manager.create_protocol()

    tl.init()

    pair_protocol(orchestrator=test_orch, clients=[test_client1, test_client2])

    test_orch.protocols[0].start(test_orch)

    for i in range(len(test_orch.protocols[0].sent_messages)):
        assert test_orch.protocols[0].sent_messages[i] is QlanMeasurementMsgType.Y_Outcome1 

def test_send_outcome_messages_x_0():
    tl = Timeline()

    test_client1 = QlanClientNode(name='test_client1',
                            tl=tl, 
                            num_local_memories=1)
    test_client2 = QlanClientNode(name='test_client2',
                            tl=tl, 
                            num_local_memories=1)
    
    test_memo1 = test_client1.get_components_by_type("Memory")[0]
    test_memo2 = test_client2.get_components_by_type("Memory")[0]

    test_orch = QlanOrchestratorNode("test_orch",
                                tl, 
                                num_local_memories=1, 
                                remote_memories=[test_memo1, test_memo2])
    test_orch.set_seed(2)
    test_orch.update_bases('x')
    
    cc_o_c1 = ClassicalChannel("cc_o_c1", tl, 10, 1e9)
    cc_o_c2 = ClassicalChannel("cc_o_c2", tl, 10, 1e9)
    cc_o_c1.set_ends(test_orch, test_client1.name)
    cc_o_c2.set_ends(test_orch, test_client2.name)

    test_orch.resource_manager.create_protocol()

    tl.init()

    pair_protocol(orchestrator=test_orch, clients=[test_client1, test_client2])

    test_orch.protocols[0].start(test_orch)

    for i in range(len(test_orch.protocols[0].sent_messages)):
        assert test_orch.protocols[0].sent_messages[i] is QlanMeasurementMsgType.X_Outcome0 or test_orch.protocols[0].sent_messages[i] is QlanB0MsgType.B0_Designation

def test_send_outcome_messages_x_1():
    tl = Timeline()

    test_client1 = QlanClientNode(name='test_client1',
                            tl=tl, 
                            num_local_memories=1)
    test_client2 = QlanClientNode(name='test_client2',
                            tl=tl, 
                            num_local_memories=1)
    
    test_memo1 = test_client1.get_components_by_type("Memory")[0]
    test_memo2 = test_client2.get_components_by_type("Memory")[0]

    test_orch = QlanOrchestratorNode("test_orch",
                                tl, 
                                num_local_memories=1, 
                                remote_memories=[test_memo1, test_memo2])
    test_orch.set_seed(0)
    test_orch.update_bases('x')
    
    cc_o_c1 = ClassicalChannel("cc_o_c1", tl, 10, 1e9)
    cc_o_c2 = ClassicalChannel("cc_o_c2", tl, 10, 1e9)
    cc_o_c1.set_ends(test_orch, test_client1.name)
    cc_o_c2.set_ends(test_orch, test_client2.name)

    test_orch.resource_manager.create_protocol()

    tl.init()

    pair_protocol(orchestrator=test_orch, clients=[test_client1, test_client2])

    test_orch.protocols[0].start(test_orch)

    for i in range(len(test_orch.protocols[0].sent_messages)):
        assert test_orch.protocols[0].sent_messages[i] is QlanMeasurementMsgType.X_Outcome1 or test_orch.protocols[0].sent_messages[i] is QlanB0MsgType.B0_Designation


def test_update_adjacent_nodes():

    def dummy_update_adjacent_nodes(current_key, adjacent_nodes, b0=None):
        saved_values = []
        keys_to_clear = []

        if b0 is not None:
            for key, values in adjacent_nodes.items():
                if b0 in values:
                    saved_values.extend([val for val in values if val != b0])
                    keys_to_clear.append(key)
            
            for key, values in adjacent_nodes.items():
                if b0 in values:
                    new_values = [val if val != b0 else saved_values for val in values]
                    new_values = [item for sublist in new_values for item in (sublist if isinstance(sublist, list) else [sublist])]
                    seen = set()
                    adjacent_nodes[key] = [x for x in new_values if not (x in seen or seen.add(x))]

        adjacent_nodes[current_key] = []
        print(f"DEBUG: updated adjacent nodes: {adjacent_nodes}")

    adjacent_nodes = {0: [0, 1], 1: [1, 2], 2: [2, 3]}
    for current_key in range(len(adjacent_nodes.keys())):
        dummy_update_adjacent_nodes(current_key, adjacent_nodes)
        assert adjacent_nodes[current_key] == []
    
    adjacent_nodes = {0: [0, 1], 1: [1, 2], 2: [2, 3]}
    b0 = 1
    for current_key in range(len(adjacent_nodes.keys())):
        if b0 in adjacent_nodes.get(current_key, []):
            dummy_update_adjacent_nodes(current_key, adjacent_nodes, b0=b0)
            assert adjacent_nodes[current_key+1] == [0, 2]
            assert adjacent_nodes[current_key+2] == [2, 3]
            assert adjacent_nodes[current_key] == []
        else:
            dummy_update_adjacent_nodes(current_key, adjacent_nodes, b0=b0)
            assert adjacent_nodes[current_key] == []