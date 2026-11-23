// THUNK ALIAS -> sub_1444E3540 (jmp:0x1415420a0->0x1444e3540)
__int64 __fastcall sub_1444E3540(__int64 **a1, __int64 *a2)
{
  __int64 v4; // rcx
  __int64 v5; // r13
  __int64 v6; // rdx
  unsigned __int64 v7; // rsi
  __int64 v8; // r15
  __int64 v9; // rbx
  unsigned __int64 v10; // rcx
  __int64 v11; // r8
  __int64 v12; // rcx
  __int64 v13; // rdi
  __int64 i; // rbx
  __int64 v15; // rsi
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // rax
  __int64 v19; // rcx
  __int64 v21; // [rsp+20h] [rbp-40h]
  __int64 v22; // [rsp+28h] [rbp-38h]
  __int64 v23; // [rsp+30h] [rbp-30h]
  __int64 v24; // [rsp+38h] [rbp-28h] BYREF
  __int64 v25; // [rsp+40h] [rbp-20h]
  unsigned __int64 v26; // [rsp+48h] [rbp-18h]
  __int64 v27; // [rsp+50h] [rbp-10h] BYREF
  __int64 v28; // [rsp+58h] [rbp-8h]
  __int64 v29; // [rsp+60h] [rbp+0h]

  v29 = -2;
  sub_1407C9510(&v24);
  v4 = **a1;
  v5 = (*a1)[1];
  v6 = v5 - v4;
  v7 = (v5 - v4) >> 3;
  if ( (__int64)(v26 - v24) >> 3 < v7 )
  {
    v22 = v24;
    v21 = **a1;
    if ( v6 < 0 )
      sub_1400526C0(v4);
    v8 = v25;
    v9 = sub_1407E4490(qword_141ABD470, v6);
    sub_141758A00();
    if ( v24 == 0 )
      goto LABEL_14;
    v10 = v26 - v24;
    if ( v26 - v24 == -1 )
    {
      v10 = *(unsigned int *)(v24 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_13;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_13;
    }
    v11 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v11) >> 3 > v10 )
    {
      v12 = *(_QWORD *)(v11 + 8 * v10);
      if ( v12 != 0 )
      {
        v23 = v12;
        MEMORY[0x1419475D8](v12 + 32, v24 - *(unsigned int *)(v12 + 120));
        if ( (*(_BYTE *)(v23 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v23 + 64)) == 0)
          && *(_BYTE *)(v23 + 97) != 0 )
        {
          sub_1412D33C0(v23);
        }
        goto LABEL_14;
      }
    }
LABEL_13:
    MEMORY[0x141948990](v24 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_14:
    v24 = v9;
    v25 = v9 + v8 - v22;
    v26 = v9 + 8 * v7;
    v4 = v21;
  }
  if ( v5 != v4 )
  {
    v13 = 1;
    if ( v7 >= 2 )
      v13 = v7;
    for ( i = 0; i != v13; ++i )
    {
      v15 = *(_QWORD *)(**a1 + 8 * i);
      if ( v15 != 0 )
      {
        v16 = sub_14083D4F0(v4);
        v28 = 0;
        v27 = v16 + 8;
        sub_141542380(v15, &v27);
        sub_14083B5F0(&v24, &v27);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
      }
    }
  }
  sub_14083DB80(&v27, &v24);
  v17 = *a2;
  if ( &v27 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v17 + 16LL))(v17, a2);
    v18 = v27;
    v19 = v28;
    a2[1] = v28;
    *a2 = v18;
    v17 = sub_14083D4F0(v19) + 8;
    v28 = 0;
    v27 = v17;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v17 + 16LL))(v17, &v27);
  return sub_14083B0A0(&v24);
}
