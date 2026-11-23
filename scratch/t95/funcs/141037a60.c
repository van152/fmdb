// THUNK ALIAS -> sub_143EBF110 (jmp:0x141037a60->0x143ebf110)
char __fastcall sub_143EBF110(__int64 a1, int *a2, int *a3, char a4, unsigned __int8 a5, __int64 *a6)
{
  unsigned int v6; // r14d
  char v9; // r15
  unsigned __int64 v10; // rsi
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rax
  __int64 v16; // rsi
  int v17; // r15d
  unsigned __int16 v18; // r14
  unsigned __int64 v19; // rdi
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v24; // rcx
  __int64 v25; // rax
  __int64 v27; // [rsp+28h] [rbp-28h] BYREF
  unsigned __int64 v28; // [rsp+30h] [rbp-20h]
  __int64 v29; // [rsp+40h] [rbp-10h] BYREF
  unsigned __int64 v30; // [rsp+48h] [rbp-8h]
  __int64 v31; // [rsp+50h] [rbp+0h]

  v31 = -2;
  LOBYTE(v6) = a4;
  v9 = a1;
  LODWORD(v28) = 1;
  v27 = sub_14083D4F0(a1) + 40;
  sub_140835380(a6, 1685353593, &v27);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
  v10 = ((unsigned __int64)(unsigned int)a2[1] << 32) | *a2;
  v12 = sub_14083D4F0(v11);
  v28 = v10;
  v27 = v12 + 72;
  sub_140835380(a6, 1685417577, &v27);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
  v14 = sub_14083D4F0(v13);
  if ( v9 != 0 )
    LODWORD(v28) = 1349804394;
  else
    LODWORD(v28) = 1349411178;
  v27 = v14 + 56;
  sub_140835380(a6, 1886549113, &v27);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
  v15 = sub_140FA3700(qword_141B5FE40, a3);
  if ( v15 != 0 )
  {
    v16 = v15;
    v17 = 0;
    if ( (_BYTE)v6 != 0 )
    {
      v18 = sub_141036DB0(v6, v15);
      if ( a5 == 0 )
        goto LABEL_11;
      goto LABEL_10;
    }
    v18 = 0;
    if ( a5 != 0 )
LABEL_10:
      v17 = (unsigned __int16)sub_141036DB0(a5, v16);
  }
  else
  {
    v18 = 0;
    v17 = 0;
  }
LABEL_11:
  sub_1407C9510(&v27);
  v19 = *a3 | ((unsigned __int64)(unsigned int)a3[1] << 32);
  v21 = sub_14083D4F0(v20);
  v30 = v19;
  v29 = v21 + 72;
  sub_140835380(&v27, 1416914273, &v29);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
  v23 = sub_14083D4F0(v22);
  LODWORD(v30) = v18;
  v29 = v23 + 56;
  sub_140835380(&v27, 1349151845, &v29);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
  v25 = sub_14083D4F0(v24);
  LODWORD(v30) = v17;
  v29 = v25 + 56;
  sub_140835380(&v27, 1349675634, &v29);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
  sub_14083DC80(&v29, &v27);
  sub_140835380(a6, 1853322860, &v29);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
  sub_140833970(&v27);
  return 1;
}
