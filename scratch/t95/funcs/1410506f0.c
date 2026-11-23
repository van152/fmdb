// THUNK ALIAS -> sub_143EE2D50 (jmp:0x1410506f0->0x143ee2d50)
__int64 __fastcall sub_143EE2D50(__int64 a1, __int64 a2)
{
  unsigned __int64 v3; // rdi
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rdx
  __int64 *v7; // rbx
  __int64 *v8; // rdx
  int v9; // eax
  __int64 v10; // rsi
  __int64 v11; // rdi
  __int64 v12; // rax
  char v13; // cl
  __int64 v14; // r13
  __int64 v15; // rdi
  __int64 v16; // rax
  char v17; // bl
  unsigned __int64 v19; // [rsp+20h] [rbp-20h]
  __int64 v21; // [rsp+30h] [rbp-10h] BYREF
  __int64 v22; // [rsp+38h] [rbp-8h]
  __int64 v23; // [rsp+40h] [rbp+0h]

  v23 = -2;
  v3 = *(_QWORD *)(**(_QWORD **)a1 + 200LL) - *(_QWORD *)(**(_QWORD **)a1 + 192LL);
  v19 = (__int16)(v3 >> 4);
  v4 = qword_141B60C38;
  v5 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_22;
  v6 = qword_141B60C30;
  while ( *(_DWORD *)v6 != 1684171881 )
  {
    v6 += 16;
    if ( v6 == qword_141B60C38 )
      goto LABEL_22;
  }
  if ( v6 == qword_141B60C38 || *(_QWORD *)(v6 + 8) == 0 )
    goto LABEL_22;
  v7 = nullptr;
  while ( *(_DWORD *)v5 != 1684171881 )
  {
    v5 += 16;
    if ( v5 == qword_141B60C38 )
      goto LABEL_15;
  }
  v7 = v5 == qword_141B60C38 ? nullptr : *(__int64 **)(v5 + 8);
LABEL_15:
  v8 = &qword_141B5A4A0;
  if ( v7 != nullptr )
    v8 = v7;
  v9 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v8 + 64LL))(*v8);
  LODWORD(v10) = v9;
  if ( v9 < 0 || v19 <= (unsigned int)v9 )
  {
LABEL_22:
    LODWORD(v10) = -1;
    if ( v3 << 44 >> 48 == 0 )
      return (unsigned int)v10;
  }
  else
  {
    v11 = *(_QWORD *)(**(_QWORD **)a1 + 192LL);
    v12 = sub_14083D4F0(v4) + 8;
    v22 = 0;
    v21 = v12;
    if ( v11 != 0 )
    {
      sub_141050200(16LL * (unsigned int)v10 + v11, &v21);
      v13 = sub_140DD6070(a2, &v21, 0);
      v12 = v21;
      if ( v13 != 0 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, &v21);
        return (unsigned int)v10;
      }
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v12 + 16LL))(v12, &v21);
  }
  v14 = 0;
  v10 = 0;
  do
  {
    v15 = *(_QWORD *)(**(_QWORD **)a1 + 192LL);
    v16 = sub_14083D4F0(v4) + 8;
    v22 = 0;
    v21 = v16;
    if ( v15 != 0 )
    {
      sub_141050200((v14 >> 28) + v15, &v21);
      v17 = sub_140DD6070(a2, &v21, 0);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, &v21);
      if ( v17 != 0 )
        return (unsigned int)v10;
    }
    else
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v16 + 16LL))(v16, &v21);
    }
    ++v10;
    v14 += 0x100000000LL;
  }
  while ( v19 != v10 );
  LODWORD(v10) = -1;
  return (unsigned int)v10;
}
