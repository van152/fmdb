char __fastcall sub_143FC68B0(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4, unsigned __int8 a5)
{
  __int64 v7; // rdx
  __int64 v8; // r9
  _QWORD **v9; // rdi
  _QWORD **i; // rbx
  __int64 v11; // rdi
  _QWORD v13[6]; // [rsp+38h] [rbp-30h] BYREF

  v13[0] = a1[7];
  if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)v13, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
    a1[7] = v13[0];
  v13[0] = a1[8];
  if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)v13, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
    a1[8] = v13[0];
  sub_140F80250(a3, a1 + 9, a5, 0);
  v9 = (_QWORD **)a1[3];
  for ( i = (_QWORD **)a1[4]; v9 != i; ++v9 )
  {
    LOBYTE(v7) = 1;
    LOBYTE(v8) = 1;
    sub_141191FD0(*v9, v7, a3, v8, a5);
  }
  v11 = a1[6];
  if ( v11 != 0 )
  {
    sub_140F80250(a3, v11 + 24, a5, 0);
    v13[0] = *(_QWORD *)(v11 + 32);
    if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)v13, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
      *(_QWORD *)(v11 + 32) = v13[0];
    v13[0] = *(_QWORD *)(v11 + 40);
    if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)v13, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
      *(_QWORD *)(v11 + 40) = v13[0];
  }
  return 1;
}
