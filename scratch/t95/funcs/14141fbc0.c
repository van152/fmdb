// THUNK ALIAS -> sub_14432C180 (jmp:0x14141fbc0->0x14432c180)
__int64 sub_14432C180()
{
  _QWORD *v0; // rsi
  __int64 result; // rax

  v0 = (_QWORD *)qword_141B63D28;
  result = sub_140051570(&qword_141B63D28, &qword_141B63D28, *(_QWORD *)(qword_141B63D28 + 8));
  v0[1] = v0;
  *v0 = v0;
  v0[2] = v0;
  qword_141B63D30 = 0;
  return result;
}
