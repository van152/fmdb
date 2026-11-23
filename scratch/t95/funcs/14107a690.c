// THUNK ALIAS -> sub_143F20E90 (jmp:0x14107a690->0x143f20e90)
__int64 __fastcall sub_143F20E90(__int64 *a1, __int64 *a2)
{
  __int64 v4; // rcx
  __int64 v5; // r13
  __int64 v6; // rsi
  __int64 v7; // rbx
  unsigned __int64 v8; // rcx
  __int64 v9; // r8
  __int64 v10; // r12
  __int64 i; // rsi
  __int64 v12; // rdi
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rax
  __int64 v16; // rcx
  __int64 v18; // [rsp+28h] [rbp-28h] BYREF
  __int64 v19; // [rsp+30h] [rbp-20h]
  __int64 v20; // [rsp+38h] [rbp-18h] BYREF
  __int64 v21; // [rsp+40h] [rbp-10h]
  __int64 v22; // [rsp+48h] [rbp-8h]
  __int64 v23; // [rsp+50h] [rbp+0h]

  v23 = -2;
  sub_1407C9510(&v20);
  v5 = v20;
  if ( (unsigned __int64)(v22 - v20) <= 0x9F )
  {
    v6 = v21;
    v7 = sub_1407E4490(qword_141ABD470, 160);
    sub_141758A00();
    if ( v20 == 0 )
    {
LABEL_13:
      v20 = v7;
      v21 = v7 + v6 - v5;
      v22 = v7 + 160;
      goto LABEL_14;
    }
    v8 = v22 - v20;
    if ( v22 - v20 == -1 )
    {
      v8 = *(unsigned int *)(v20 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](v20 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v9 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v9) >> 3 > v8 )
    {
      v10 = *(_QWORD *)(v9 + 8 * v8);
      if ( v10 != 0 )
      {
        MEMORY[0x1419475D8](v10 + 32, v20 - *(unsigned int *)(v10 + 120));
        if ( (*(_BYTE *)(v10 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v10 + 64)) == 0)
          && *(_BYTE *)(v10 + 97) != 0 )
        {
          sub_1412D33C0(v10);
        }
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_14:
  for ( i = 0; i != 320; i += 16 )
  {
    v12 = *a1;
    v13 = sub_14083D4F0(v4);
    v19 = 0;
    v18 = v13 + 8;
    sub_1410792D0(i + v12, &v18);
    sub_14083B5F0(&v20, &v18);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v18 + 16LL))(v18, &v18);
  }
  sub_14083DB80(&v18, &v20);
  v14 = *a2;
  if ( &v18 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, a2);
    v15 = v18;
    v16 = v19;
    a2[1] = v19;
    *a2 = v15;
    v14 = sub_14083D4F0(v16) + 8;
    v19 = 0;
    v18 = v14;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v18);
  return sub_14083B0A0(&v20);
}
