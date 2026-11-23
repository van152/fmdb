char sub_143C557F0()
{
  _DWORD *v0; // rdx
  bool v1; // si
  __int64 v2; // rcx

  if ( qword_141B602E8 == qword_141B602F0 )
  {
    v1 = false;
  }
  else
  {
    v0 = (_DWORD *)(qword_141B602E8 + 20);
    if ( (unsigned __int64)(qword_141B602F0 - qword_141B602E8) < 0x15 )
      v0 = (_DWORD *)qword_141B602E8;
    v1 = *v0 == 1000002;
  }
  v2 = 0x1419435F1LL;
  if ( qword_141B60328 != 0 )
    v2 = qword_141B60328 + 4;
  return v1 & ((unsigned int)sub_141758D90(v2, 0x141936788LL) == 0);
}
