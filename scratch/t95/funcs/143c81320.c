__int64 __fastcall sub_143C81320(__int64 a1, __int64 *a2)
{
  _QWORD *v4; // rax
  unsigned __int64 v5; // rcx
  __int64 v6; // rax
  unsigned __int64 v7; // r13
  __int64 v8; // r15
  unsigned __int64 v9; // rcx
  __int64 v10; // rsi
  __int64 v11; // rbx
  unsigned __int64 v12; // rcx
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v17; // r8
  __int64 v18; // rcx
  bool v19; // al
  __int64 v20; // rdi
  _QWORD *v21; // rax
  __int64 v22; // rsi
  __int64 v23; // rax
  __int64 v24; // [rsp+20h] [rbp-30h]
  __int64 v25; // [rsp+28h] [rbp-28h] BYREF
  __int64 v26; // [rsp+30h] [rbp-20h]
  __int64 v27; // [rsp+38h] [rbp-18h]
  __int64 v28; // [rsp+40h] [rbp-10h] BYREF
  __int64 v29; // [rsp+48h] [rbp-8h]
  __int64 v30; // [rsp+50h] [rbp+0h]

  v30 = -2;
  sub_1407C9510(&v25);
  v4 = *(_QWORD **)(**(_QWORD **)a1 + 312LL);
  if ( v4 == nullptr )
    goto LABEL_9;
  v5 = v4[1] - *v4;
  v6 = v5 << 53;
  v7 = (char)(v5 >> 3);
  v8 = v25;
  v9 = (v27 - v25) >> 3;
  if ( v9 >= v7 )
  {
    if ( HIBYTE(v6) == 0 )
      goto LABEL_9;
    goto LABEL_19;
  }
  if ( v6 < 0 )
    sub_1400526C0(v9);
  v10 = v26;
  v11 = sub_1407E4490(qword_141ABD470, 8 * v7);
  sub_141758A00();
  if ( v25 != 0 )
  {
    v12 = v27 - v25;
    if ( v27 - v25 == -1 )
    {
      v12 = *(unsigned int *)(v25 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_17:
        MEMORY[0x141948990](v25 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_18;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_17;
    }
    v17 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > v12 )
    {
      v18 = *(_QWORD *)(v17 + 8 * v12);
      if ( v18 != 0 )
      {
        v24 = v18;
        MEMORY[0x1419475D8](v18 + 32, v25 - *(unsigned int *)(v18 + 120));
        v9 = v24;
        v19 = *(_BYTE *)(v24 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24 + 64)) != 0;
        if ( !v19 && *(_BYTE *)(v24 + 97) != 0 )
          sub_1412D33C0(v24);
        goto LABEL_18;
      }
    }
    goto LABEL_17;
  }
LABEL_18:
  v25 = v11;
  v26 = v11 + v10 - v8;
  v27 = v11 + 8 * v7;
LABEL_19:
  v20 = 0;
  do
  {
    v21 = *(_QWORD **)(**(_QWORD **)a1 + 312LL);
    if ( v21 != nullptr )
    {
      v22 = *(_QWORD *)(*v21 + 8 * v20);
      if ( v22 != 0 )
      {
        v23 = sub_14083D4F0(v9);
        v29 = 0;
        v28 = v23 + 8;
        sub_140EABBE0(v22, &v28, 0);
        sub_14083B5F0(&v25, &v28);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v28 + 16LL))(v28, &v28);
      }
    }
    ++v20;
  }
  while ( v7 != v20 );
LABEL_9:
  sub_14083DB80(&v28, &v25);
  v13 = *a2;
  if ( &v28 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13 + 16LL))(v13, a2);
    v14 = v28;
    v15 = v29;
    a2[1] = v29;
    *a2 = v14;
    v13 = sub_14083D4F0(v15) + 8;
    v29 = 0;
    v28 = v13;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13 + 16LL))(v13, &v28);
  return sub_14083B0A0(&v25);
}
