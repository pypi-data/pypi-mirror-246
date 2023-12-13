from tpltable.utils import *
from tpltable.table_io import TableIO

class TableFlowNet:
    """
    控制table处理流程的类
    """
    ...

tTABLE = TableIO
tN2DICT = np.ndarray
TYPES = [tTABLE, tN2DICT]

class _TableFlowNode:
    """
    流程操作类
    包含一组函数：
    * 除开第一个函数，其余函数的参数均为上一个函数的返回值

    """
    def __init__(self, inputs:list=None, outputs:list=None, funcs:list=None, select:list=None):
        """
        inputs: 输入参数列表, 用于检查和推断参数类型
        outputs: 输出参数列表，用于检查和推断参数类型（只作用于最后一个函数）
        funcs: 操作函数列表
        select: 选择函数返回值列表，用于检查和推断参数类型
        """
        self.inputs = inputs if inputs else []
        self.outputs = outputs if outputs else []
        self.funcs = funcs if funcs else []
        self.select = select if select else []

    def config(self, inputs:list=None, outputs:list=None, funcs:list=None):
        """
        配置流程操作
        """
        if inputs:
            self.inputs = inputs
        if outputs:
            self.outputs = outputs
        if funcs:
            self.funcs = funcs

    def __call__(self, inputs:list):
        # check inputs
        if len(inputs) != len(self.inputs):
            log.error(f'inputs length error: got:{len(inputs)} != expected:{len(self.inputs)}')
        for i, (_type, item) in enumerate(zip(self.inputs, inputs)):
            if not isinstance(item, _type):
                raise TypeError(f'input type error: index:{i}: {item} is not type:{_type}')

        # run funcs
        outputs = []
        for func in self.funcs:
            outputs.append(func(*inputs))
            inputs = outputs[-1]

