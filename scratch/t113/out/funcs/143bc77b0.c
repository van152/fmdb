char __fastcall sub_143BC77B0(__int64 a1, __int64 *a2)
{
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rdx
  __int64 v7; // rcx
  __int64 v8; // rax
  _QWORD *v9; // rax
  unsigned __int64 v10; // rbx
  __int64 v11; // r15
  __int64 v12; // r13
  __int64 v13; // r14
  __int64 v14; // rsi
  unsigned __int64 v15; // rcx
  __int64 v16; // r8
  __int64 v17; // rcx
  __int64 v18; // rsi
  bool v19; // al
  unsigned __int64 v20; // rbx
  unsigned __int64 v21; // r15
  __int64 v22; // rsi
  _BYTE v24[24]; // [rsp+28h] [rbp-38h] BYREF
  _QWORD v25[2]; // [rsp+40h] [rbp-20h] BYREF
  __int64 v26; // [rsp+50h] [rbp-10h]
  __int64 v27; // [rsp+58h] [rbp-8h]
  __int64 v28; // [rsp+60h] [rbp+0h]

  v28 = -2;
  v4 = *(int *)(*(_QWORD *)(a1 + 8) + 4LL);
  v5 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(a1 + v4 + 8) + 656LL))(a1 + v4 + 8);
  if ( v5 == 0 )
  {
    v8 = 0;
    goto LABEL_6;
  }
  v27 = 0;
  if ( *(_BYTE *)(v5 + 47) == 0 )
  {
    v7 = *(_QWORD *)(v5 + 48);
    if ( v7 != 0 )
    {
      LOBYTE(v6) = 1;
      v8 = sub_1411E6040(v7, v6, 0);
LABEL_6:
      v27 = v8;
    }
  }
  v9 = *(_QWORD **)(a1 + 248);
  if ( v9 == nullptr )
    return 1;
  v10 = (__int64)(v9[1] - *v9) >> 3;
  v11 = *a2;
  if ( (a2[2] - *a2) >> 3 < v10 )
  {
    if ( (__int64)(v9[1] - *v9) < 0 )
      sub_1400526C0();
    v12 = a2[1];
    v13 = sub_1407E4490(qword_141ABD470);
    sub_141758A00(v13, *a2, a2[1] - *a2);
    v14 = *a2;
    if ( *a2 != 0 )
    {
      v15 = a2[2] - v14;
      if ( v15 == -1 )
      {
        v15 = *(unsigned int *)(v14 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_21:
          MEMORY[0x141948990](v14 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_22;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_21;
      }
      v16 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v16) >> 3 <= v15 )
        goto LABEL_21;
      v17 = *(_QWORD *)(v16 + 8 * v15);
      if ( v17 == 0 )
        goto LABEL_21;
      v18 = v14 - *(unsigned int *)(v17 + 120);
      v26 = v17;
      MEMORY[0x1419475D8](v17 + 32, v18);
      v19 = *(_BYTE *)(v26 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 + 64)) != 0;
      if ( !v19 && *(_BYTE *)(v26 + 97) != 0 )
        sub_1412D33C0();
    }
LABEL_22:
    *a2 = v13;
    a2[1] = v13 + v12 - v11;
    a2[2] = v13 + 8 * v10;
    v9 = *(_QWORD **)(a1 + 248);
    if ( v9 == nullptr )
      return 1;
    goto LABEL_23;
  }
  if ( v9[1] == *v9 )
    return 1;
LABEL_23:
  v20 = v10 - 1;
  v21 = 0;
LABEL_24:
  if ( (__int64)(v9[1] - *v9) >> 3 > v21 )
  {
    v22 = *(_QWORD *)(*v9 + 8 * v21);
    if ( v22 != 0 )
    {
      sub_1407C9510(v24);
      sub_14146ECD0(v22, a1, v27, v24);
      sub_14083DDA0(v25, v24);
      sub_14083B5F0(a2, v25);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v25[0] + 16LL))(v25[0], v25);
      sub_140833970(v24);
    }
  }
  while ( v20 != v21 )
  {
    v9 = *(_QWORD **)(a1 + 248);
    ++v21;
    if ( v9 != nullptr )
      goto LABEL_24;
  }
  return 1;
}
