char __fastcall sub_143C07E80(__int64 a1, __int64 a2, unsigned int a3, __int64 a4)
{
  _QWORD *v8; // rsi
  __int64 v10; // [rsp+30h] [rbp-28h] BYREF

  v10 = *(_QWORD *)(a1 + 16);
  if ( (unsigned __int8)sub_140F7EE40(a2, (unsigned int)&v10, *(_QWORD *)(a2 + 152), a3, 1, 1) != 0 )
    *(_QWORD *)(a1 + 16) = v10;
  v8 = (_QWORD *)(a1 + 8);
  if ( a4 != 0 )
    *v8 = a4;
  else
    sub_140F80250(a2, v8, a3, 0);
  return 1;
}
