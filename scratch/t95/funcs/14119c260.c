// THUNK ALIAS -> sub_143FC74D0 (jmp:0x14119c260->0x143fc74d0)
__int64 __fastcall sub_143FC74D0(__int64 **a1, __int64 a2)
{
  __int64 v4; // rax
  __int64 v5; // rdi
  __int64 v6; // rbx
  unsigned __int64 v7; // r13
  __int64 v8; // rcx
  __int64 v9; // rax
  __int64 v10; // rdx
  __int64 *v11; // rsi
  __int64 *v12; // rdx
  __int64 v13; // rsi
  __int64 v14; // rcx
  __int64 v15; // rdi
  __int64 v16; // rax
  char v17; // cl
  __int64 v18; // rdi
  __int64 v19; // rax
  char v20; // bl
  __int64 v22; // [rsp+20h] [rbp-10h] BYREF
  __int64 v23; // [rsp+28h] [rbp-8h]
  __int64 v24; // [rsp+30h] [rbp+0h]

  v24 = -2;
  v4 = **a1;
  v5 = *(_QWORD *)(v4 + 24);
  v6 = *(_QWORD *)(v4 + 32);
  v7 = (v6 - v5) >> 3;
  v8 = qword_141B60C38;
  v9 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_22;
  v10 = qword_141B60C30;
  while ( *(_DWORD *)v10 != 1684171881 )
  {
    v10 += 16;
    if ( v10 == qword_141B60C38 )
      goto LABEL_22;
  }
  if ( v10 == qword_141B60C38 || *(_QWORD *)(v10 + 8) == 0 )
    goto LABEL_22;
  v11 = nullptr;
  while ( *(_DWORD *)v9 != 1684171881 )
  {
    v9 += 16;
    if ( v9 == qword_141B60C38 )
      goto LABEL_15;
  }
  v11 = v9 == qword_141B60C38 ? nullptr : *(__int64 **)(v9 + 8);
LABEL_15:
  v12 = &qword_141B5A4A0;
  if ( v11 != nullptr )
    v12 = v11;
  LODWORD(v13) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v12 + 64LL))(*v12);
  if ( (int)v13 < 0 || v7 <= (unsigned int)v13 )
  {
LABEL_22:
    if ( v6 == v5 )
    {
LABEL_29:
      LODWORD(v13) = -1;
      return (unsigned int)v13;
    }
LABEL_23:
    v13 = 0;
    while ( 1 )
    {
      v18 = *(_QWORD *)(*(_QWORD *)(**a1 + 24) + 8 * v13);
      v19 = sub_14083D4F0(v8) + 8;
      v23 = 0;
      v22 = v19;
      if ( v18 != 0 )
      {
        sub_14119C030(v18, &v22);
        v20 = sub_140DD6070(a2, &v22, 0);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
        if ( v20 != 0 )
          return (unsigned int)v13;
      }
      else
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, &v22);
      }
      if ( v7 == ++v13 )
        goto LABEL_29;
    }
  }
  v14 = *(_QWORD *)(**a1 + 24);
  v15 = *(_QWORD *)(v14 + 8LL * (unsigned int)v13);
  v16 = sub_14083D4F0(v14) + 8;
  v23 = 0;
  v22 = v16;
  if ( v15 == 0 || (sub_14119C030(v15, &v22), v17 = sub_140DD6070(a2, &v22, 0), v16 = v22, v17 == 0) )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v16 + 16LL))(v16, &v22);
    goto LABEL_23;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
  return (unsigned int)v13;
}
