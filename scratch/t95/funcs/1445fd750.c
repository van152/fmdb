__int64 __fastcall sub_1445FD750(__int64 *a1)
{
  __int64 v2; // r14
  unsigned __int64 v3; // rdi
  __int64 *v4; // rcx
  __int64 v5; // rax
  unsigned __int64 v6; // rcx
  __int64 v7; // rbx
  int v8; // ebx
  __int64 v9; // rcx
  __int64 v10; // rax
  __int64 *v11; // rbx
  __int64 v12; // rdi
  int v14; // [rsp+28h] [rbp-28h] BYREF
  _QWORD v15[2]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v16; // [rsp+40h] [rbp-10h] BYREF
  int v17; // [rsp+48h] [rbp-8h]
  __int64 v18; // [rsp+50h] [rbp+0h]

  v18 = -2;
  v15[1] = 0x76C0001076C0001LL;
  v2 = 0;
  v3 = 0;
  while ( 1 )
  {
    v4 = *(__int64 **)(qword_141B5FE60 + 128);
    v5 = *v4;
    if ( v3 >= (v4[1] - *v4) >> 3 )
      return v2;
    v6 = v3 & 0x7FFFFFFF;
    if ( (_BYTE)word_141B60320 != 0
      || (v7 = *(_QWORD *)(qword_141B5FE60 + 96), (*(_QWORD *)(qword_141B5FE60 + 104) - v7) >> 3 <= v6) )
    {
      v7 = v5;
    }
    v8 = *(_DWORD *)(*(_QWORD *)(v7 + 8 * v6) + 12LL);
    if ( sub_141048140(*a1, v8, -1, -1) == nullptr )
    {
      v17 = v8;
      v16 = sub_14083D4F0(v9) + 40;
      v12 = qword_141B5FE60;
      sub_140FE7960((__int64)&v14, &v16, 0x6167726Du);
      v15[0] = sub_140FA3700(v12, &v14);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v16 + 16LL))(v16, &v16);
      sub_14104DD70(*a1, v15);
      return 16LL * (__int16)((*(_DWORD *)(*a1 + 200) - (unsigned int)*(_QWORD *)(*a1 + 192)) >> 4)
           + *(_QWORD *)(*a1 + 192)
           - 16;
    }
    v10 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_13;
    while ( *(_DWORD *)v10 != 1986359923 )
    {
      v10 += 16;
      if ( v10 == qword_141B60C38 )
        goto LABEL_13;
    }
    if ( v10 == qword_141B60C38 )
LABEL_13:
      v11 = nullptr;
    else
      v11 = *(__int64 **)(v10 + 8);
    if ( v11 == nullptr )
      v11 = &qword_141B5A4A0;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v11 + 8LL))(*v11, v11) != 0 )
    {
      ++v3;
      if ( (*(int (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v11 + 64LL))(*v11, v11) > 3565 )
        continue;
    }
    return v2;
  }
}
