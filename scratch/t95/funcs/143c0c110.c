char __fastcall sub_143C0C110(__int64 a1, __int64 a2, __int64 a3, __int64 a4, unsigned __int8 a5)
{
  char v7; // bl
  _QWORD v9[5]; // [rsp+30h] [rbp-28h] BYREF

  v9[0] = *(_QWORD *)(a1 + 32);
  v7 = sub_140F7EE40(a3, (unsigned int)v9, *(_QWORD *)(a3 + 152), a5, 1, 1);
  if ( v7 != 0 )
    *(_QWORD *)(a1 + 32) = v9[0];
  v9[0] = *(_QWORD *)(a1 + 40);
  if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)v9, *(_QWORD *)(a3 + 152), a5, 1, 1) != 0 )
    *(_QWORD *)(a1 + 40) = v9[0];
  sub_140F7EC80(a3, a1 + 48, *(_QWORD *)(a3 + 40), a5, 1, 1);
  sub_140F7EC80(a3, a1 + 56, *(_QWORD *)(a3 + 40), a5, 1, 1);
  if ( v7 != 0 )
    sub_140E50250(a1);
  return 1;
}
