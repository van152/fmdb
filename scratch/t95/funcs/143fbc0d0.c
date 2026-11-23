char __fastcall sub_143FBC0D0(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4, unsigned __int8 a5)
{
  _QWORD *v7; // rbx
  _QWORD *v8; // rdi
  _QWORD v10[5]; // [rsp+30h] [rbp-28h] BYREF

  sub_140F80250(a3, a1 + 9, a5, 0);
  v10[0] = a1[10];
  if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)v10, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
    a1[10] = v10[0];
  v10[0] = a1[11];
  if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)v10, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
    a1[11] = v10[0];
  v7 = (_QWORD *)a1[3];
  v8 = (_QWORD *)a1[4];
  while ( v7 != v8 )
  {
    if ( *v7 != 0 )
      sub_140F7EC80(a3, *v7, *(_QWORD *)(a3 + 24), a5, 1, 0);
    ++v7;
  }
  return 1;
}
