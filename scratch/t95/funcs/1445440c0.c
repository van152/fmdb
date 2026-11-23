char __fastcall sub_1445440C0(__int64 a1, __int64 a2, __int64 a3, char a4, unsigned __int8 a5)
{
  __int64 v8; // [rsp+38h] [rbp-20h] BYREF

  if ( a4 != 0 )
  {
    sub_140F80250(a3, a1 + 24, a5, 0);
    v8 = *(_QWORD *)(a1 + 32);
    if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)&v8, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
      *(_QWORD *)(a1 + 32) = v8;
  }
  return 1;
}
