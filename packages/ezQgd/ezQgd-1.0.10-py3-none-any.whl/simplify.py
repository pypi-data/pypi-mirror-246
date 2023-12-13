import re
import math
import traceback
from qiskit import Aer
from qiskit import transpile
from qiskit import QuantumCircuit


class Const(object):
    RZ_PERIOD = 2 * math.pi
    RZ_PARAMS = {
            "-pi/2": -math.pi/2,
            "pi/2": math.pi/2,
            "-pi": math.pi,
            "pi": math.pi
    }
    SIMPLIFY_RULE = {
        "rz_param_as_pi": {
            r'RZ Q(\d+) -pi(\n|$)': "RZ Q[1] pi",
            r"RZ Q(\d+) pi(\n|$)": "RZ Q[1] pi/2\nRZ Q[1] pi/2"
        },
        "gate_conversion": {
            r"Y2M Q(\d+)\nY2P Q\1": "I Q[1] 0",
            r"Y2P Q(\d+)\nY2M Q\1": "I Q[1] 0",
            r"X2M Q(\d+)\nX2P Q\1": "I Q[1] 0",
            r"X2P Q(\d+)\nX2M Q\1": "I Q[1] 0",
            r'Y2M Q(\d+)\nY2M Q\1\nY2M Q\1': "Y2P Q[1]",
            r'Y2P Q(\d+)\nY2P Q\1\nY2P Q\1': "Y2M Q[1]",
            r'X2M Q(\d+)\nX2M Q\1\nX2M Q\1': "X2P Q[1]",
            r'X2P Q(\d+)\nX2P Q\1\nX2P Q\1': "X2M Q[1]"
        },
        "gate_param_conversion": {
            r"Y2P Q(\d+)\nX2M Q\1": "X2M Q[1]\nRZ Q[1] pi/2",
            r"Y2M Q(\d+)\nX2M Q\1": "X2M Q[1]\nRZ Q[1] -pi/2",
            r"Y2M Q(\d+)\nX2P Q\1": "X2P Q[1]\nRZ Q[1] pi/2",
            r"Y2P Q(\d+)\nX2P Q\1": "X2P Q[1]\nRZ Q[1] -pi/2", 
            r"X2P Q(\d+)\nY2P Q\1": "Y2P Q[1]\nRZ Q[1] pi/2",
            r"X2P Q(\d+)\nY2M Q\1": "Y2M Q[1]\nRZ Q[1] -pi/2",
            r"X2M Q(\d+)\nY2M Q\1": "Y2M Q[1]\nRZ Q[1] pi/2",
            r"X2M Q(\d+)\nY2P Q\1": "Y2P Q[1]\nRZ Q[1] -pi/2",
            r"RZ Q(\d+) pi/2\nX2P Q\1": "Y2P Q[1]\nRZ Q[1] pi/2",
            r"RZ Q(\d+) pi/2\nX2M Q\1": "Y2M Q[1]\nRZ Q[1] pi/2",
            r"RZ Q(\d+) -pi/2\nX2P Q\1": "Y2M Q[1]\nRZ Q[1] -pi/2",
            r"RZ Q(\d+) -pi/2\nX2M Q\1": "Y2P Q[1]\nRZ Q[1] -pi/2",
            r"RZ Q(\d+) pi/2\nY2P Q\1": "X2M Q[1]\nRZ Q[1] pi/2",
            r"RZ Q(\d+) pi/2\nY2M Q\1": "X2P Q[1]\nRZ Q[1] pi/2",     
            r"RZ Q(\d+) -pi/2\nY2P Q\1": "X2P Q[1]\nRZ Q[1] -pi/2",
            r"RZ Q(\d+) -pi/2\nY2M Q\1": "X2M Q[1]\nRZ Q[1] -pi/2"
        },        
        "rz_param_conversion": {
            r'Y2P Q(\d+)\nY2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2P Q\1': "RZ Q[1] -[2]\nY2M Q[1]",
            r"Y2P Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nY2P Q\1\nY2P Q\1": "Y2M Q[1]\nRZ Q[1] -[2]",
            r"Y2P Q(\d+)\nY2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2M Q\1": "RZ Q[1] -[2]\nY2P Q[1]",
            r"Y2P Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nY2M Q\1\nY2M Q\1": "Y2M Q[1]\nRZ Q[1] -[2]",
            r"Y2M Q(\d+)\nY2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2P Q\1": "RZ Q[1] -[2]\nY2M Q[1]",
            r"Y2M Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nY2P Q\1\nY2P Q\1": "Y2P Q[1]\nRZ Q[1] -[2]",
            r"Y2M Q(\d+)\nY2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2M Q\1": "RZ Q[1] -[2]\nY2P Q[1]",
            r"Y2M Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nY2M Q\1\nY2M Q\1": "Y2P Q[1]\nRZ Q[1] -[2]",
            r"X2P Q(\d+)\nX2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2P Q\1": "RZ Q[1] -[2]\nX2M Q[1]",
            r"X2P Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nX2P Q\1\nX2P Q\1": "X2M Q[1]\nRZ Q[1] -[2]",
            r"X2P Q(\d+)\nX2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2M Q\1": "RZ Q[1] -[2]\nX2P Q[1]",
            r"X2P Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nX2M Q\1\nX2M Q\1": "X2M Q[1]\nRZ Q[1] -[2]",
            r"X2M Q(\d+)\nX2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2P Q\1": "RZ Q[1] -[2]\nX2M Q[1]",
            r"X2M Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nX2P Q\1\nX2P Q\1": "X2P Q[1]\nRZ Q[1] -[2]",
            r"X2M Q(\d+)\nX2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2M Q\1": "RZ Q[1] -[2]\nX2P Q[1]",
            r"X2M Q(\d+)\nRZ Q\1 (\d+(\.\d*)?)\nX2M Q\1\nX2M Q\1": "X2P Q[1]\nRZ [1] -[2]",
            r"Y2M Q(\d+)\nX2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2P Q\1\nX2P Q\1": "X2M Q[1]\nRZ Q[1] [2]\nX2P Q[1]",
            r"Y2P Q(\d+)\nX2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2P Q\1\nY2M Q\1": "X2M Q[1]\nRZ Q[1] [2]\nX2P Q[1]",
            r"Y2M Q(\d+)\nX2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2M Q\1\nY2P Q\1": "X2P Q[1]\nRZ Q[1] [2]\nX2M Q[1]",
            r"Y2P Q(\d+)\nX2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nX2M Q\1\nY2M Q\1": "X2P Q[1]\nRZ Q[1] [2]\nX2M Q[1]",
            r"X2M Q(\d+)\nY2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2M Q\1\nX2P Q\1": "Y2P Q[1]\nRZ Q[1] [2]\nY2M Q[1]",
            r"X2P Q(\d+)\nY2P Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2M Q\1\nX2M Q\1": "Y2P Q[1]\nRZ Q[1] [2]\nY2M Q[1]",
            r"X2M Q(\d+)\nY2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2P Q\1\nY2P Q\1": "Y2M Q[1]\nRZ Q[1] [2]\nY2P Q[1]",
            r"X2P Q(\d+)\nY2M Q\1\nRZ Q\1 (\d+(\.\d*)?)\nY2P Q\1\nX2M Q\1": "Y2M Q[1]\nRZ Q[1] [2]\nY2P Q[1]"
        }
    }


class QCIS_Simplify():
    def __init__(self):
        self.const = Const()
        self.simplify_rule = self.const.SIMPLIFY_RULE
        self.check_rule_list = [
            'rz_param_conversion',
            'gate_param_conversion',
            'gate_conversion'
        ]
        self.rz_period = self.const.RZ_PERIOD
        self.rz_params = self.const.RZ_PARAMS
        
    def find_qubit_by_qasm(self, conversion_value):
        params_idx = re.findall(r'\[(\d+)\]', conversion_value)
        params_idx = list(set(params_idx))
        return params_idx
    
    def replace_conversion(self, rz_pi_flag=False):
        # 根据rz_param_conversion替换现有的qics，完成rz部分化简
        # gate_param_conversion gate_conversion都是类似的
        if rz_pi_flag is False:
            check_rule_list = self.check_rule_list
        else:
            check_rule_list = ['rz_param_as_pi']
        for rule in check_rule_list:
            for conversion_key, conversion_value in self.simplify_rule[rule].items():
                pattern = re.compile(conversion_key)
                matches = pattern.finditer(self.qcis_instr)
                params_idx = self.find_qubit_by_qasm(conversion_value)
                for match in matches:
                    new_string = conversion_value
                    full_match = match.group(0)
                    # 替换化简
                    for idx in params_idx:
                        new_string = new_string.replace(f'[{idx}]', match.group(int(idx)))
                    
                    # rz_param_as_pi转换后可能需要添加\n
                    if rz_pi_flag:
                        has_newline = bool(match.group(2))
                        has_newline = '\n' if has_newline else ''
                        new_string = f'{new_string}{has_newline}'
                    self.qcis_instr = self.qcis_instr.replace(full_match, new_string)
    
    def check_conversion(self):
        # 检查是否需要rz_param_conversion化简，一旦检查出有匹配的立马返回，进行化简
        # 如果都没有匹配的，返回False进行下一步检查
        for rule in self.check_rule_list:
            for conversion_key, _ in self.simplify_rule[rule].items():
                pattern = re.compile(conversion_key)
                matches = pattern.finditer(self.qcis_instr)
                if len(list(matches)) > 0:
                    return True
        return False
        
    # Check if optimization can continue
    def check_optimization_continue(self):
        flag = self.check_conversion()
        if flag:
            self.replace_conversion()
        return flag
    
    def repeat_rz(self):
        # 将rz_params参数替换成具体值
        for param_key, param_value in self.rz_params.items():
            self.qcis_instr = self.qcis_instr.replace(param_key, str(param_value))
        # 处理重复的RZ
        # 定义正则表达式模式
        pattern = re.compile(r'(RZ Q(\d+) ([^\n]+)\n)(RZ Q\2 ([^\n]+)\n?)+')

        # 查找匹配的连续RZ门，合并参数
        matches = pattern.finditer(self.qcis_instr)
        for match in matches:
            full_match = match.group(0)
            q_number = match.group(2)
            parameters = match.group(3).split()
            # 计算连续参数的和
            parameters = [r.split(' ')[-1] for r in full_match.split('\n') if r]
            total_parameter = sum(float(param) for param in parameters)
            
            if total_parameter == -math.pi:
                total_parameter = math.pi
            if total_parameter > math.pi or total_parameter < -math.pi:
                total_parameter = total_parameter % (self.rz_period)
                # 如果取模2π的结果大于π，再进行-2π取模
                if total_parameter > math.pi:
                    total_parameter = total_parameter % (-self.rz_period)
            
            # 构建新的RZ字符串
            new_rz = f'RZ Q{q_number} {total_parameter}\n'
            # 替换原始字符串中的匹配部分
            self.qcis_instr = self.qcis_instr.replace(full_match, new_rz, 1)
        
    def simplify(self, qcis):
        try:
            self.qcis_instr = '\n'.join([q.strip() for q in qcis.split('\n')])
            # 线路化简一开始需要先替换线路中RZ(π)
            # RZ(-π) -- > RZ(π) -- > RZ(π/2)RZ(π/2)
            # 因为RZ部分化简都基于参数为π/2来化简的
            self.replace_conversion(rz_pi_flag=True)
            while True:
                is_simplify = self.check_optimization_continue()
                # 没有能继续优化了的，返回最终的qcis
                if not is_simplify:
                    self.repeat_rz()
                    return self.qcis_instr
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return qcis


class QASM_Simplify():
    def simplify(self, qasm_str):
        try:
            qc = QuantumCircuit.from_qasm_str(qasm_str)
            backend = Aer.get_backend('aer_simulator')
            qc_t = transpile(qc, backend)
            basis_gates = ["rz", "h", "cx"]
            qc_t_2 = transpile(qc_t, basis_gates=basis_gates)
            simplify_qasm = qc_t_2.qasm(encoding='utf_8')
            return simplify_qasm
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return qasm_str
