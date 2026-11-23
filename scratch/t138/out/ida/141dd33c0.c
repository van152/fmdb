__int64 __fastcall sub_141DD33C0(__int64 a1, int a2)
{
  int *v2; // rdi
  __int64 v4; // rcx
  __int64 v5; // rdi
  __int64 v6; // rcx
  __int64 v8; // rdi
  __int64 v9; // rdi
  char v10; // al
  __int64 v11; // rsi
  __int64 v12; // rax
  __int64 v13; // rcx
  void (__fastcall ***v14)(_QWORD, __int64); // rcx
  char v15; // [rsp+4Eh] [rbp-7Ah] BYREF
  char v16; // [rsp+4Fh] [rbp-79h] BYREF
  __int64 v17; // [rsp+50h] [rbp-78h] BYREF
  __int64 v18; // [rsp+58h] [rbp-70h] BYREF
  int v19; // [rsp+60h] [rbp-68h] BYREF
  _BYTE v20[8]; // [rsp+68h] [rbp-60h] BYREF
  int v21; // [rsp+70h] [rbp-58h]
  bool v22; // [rsp+74h] [rbp-54h]
  bool v23; // [rsp+75h] [rbp-53h]
  char v24; // [rsp+76h] [rbp-52h]
  __int16 v25; // [rsp+77h] [rbp-51h]
  char v26; // [rsp+79h] [rbp-4Fh]
  char v27; // [rsp+7Ah] [rbp-4Eh]
  char v28; // [rsp+7Bh] [rbp-4Dh]
  _BYTE v29[8]; // [rsp+80h] [rbp-48h] BYREF
  _BYTE v30[4]; // [rsp+88h] [rbp-40h] BYREF
  unsigned __int16 v31; // [rsp+8Ch] [rbp-3Ch]
  _BYTE v32[56]; // [rsp+90h] [rbp-38h] BYREF

  LODWORD(v2) = a2;
  sub_1407D0D60(a1: v30);
  sub_1407D0F70(
    a1: (unsigned int)v30,
    a2: (unsigned int)&v17,
    a3: (_DWORD)v2,
    a4: (unsigned int)&unk_141ABEA70,
    a5: (__int64)&unk_141B59880,
    a6: 0,
    a7: 0,
    0);
  if ( v17 == 0 )
  {
    LOBYTE(v2) = 1;
    LOBYTE(v4) = 1;
    sub_140F636B0(a1: v4);
    v6 = v17;
    if ( v17 == 0 )
      return (unsigned int)v2;
    goto LABEL_8;
  }
  sub_140310A50(a1: v29);
  sub_140814B10(a1: v17, a2: &v19, a3: v29);
  if ( v19 != 0 )
    goto LABEL_4;
  v5 = v17;
  (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v17 + 40LL))(a1: v17, a2: &v16, a3: 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    goto LABEL_4;
  if ( v31 < 8u )
  {
    byte_141A80840 = 0;
    v15 = 0;
  }
  else
  {
    v8 = v17;
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v17 + 40LL))(a1: v17, a2: &byte_141A80840, a3: 1);
    if ( *(_DWORD *)(v8 + 16) != 0
      || (v15 = 0, v31 >= 9u)
      && (v9 = v17,
          (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v17 + 40LL))(a1: v17, a2: &v15, a3: 1),
          *(_DWORD *)(v9 + 16) != 0) )
    {
LABEL_4:
      LODWORD(v2) = 0;
      goto LABEL_5;
    }
  }
  v10 = v16;
  *(_BYTE *)(a1 + 1363) = v16 == 2;
  *(_BYTE *)(a1 + 1347) = v10 != 4;
  v2 = &v19;
  sub_140310A50(a1: &v19);
  sub_140310A50(a1: v20);
  v21 = 124518401;
  v26 = 0;
  v27 = 0;
  v22 = v16 == 4;
  v23 = v16 == 3;
  v25 = v16 == 2;
  v24 = 1;
  v28 = v15;
  sub_1407C2920(a1: v32, a2: v29);
  sub_140F961C0(a1: &v18, a2: v32, a3: &v19);
  v11 = v18;
  if ( v18 != 0 )
  {
    v2 = (int *)qword_141ABDFE8;
    v12 = sub_140843600();
    sub_1408436D0(a1: v12, a2: v32, a3: &v18);
    sub_140801DF0(a1: v2, a2: &unk_141B5E3C0, a3: v32, a4: 0);
    sub_14083D320(a1: v32);
    LOBYTE(v13) = 1;
    sub_140F636B0(a1: v13);
    v14 = (void (__fastcall ***)(_QWORD, __int64))v18;
    if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 8)) == 0 )
      (**v14)(a1: v14, a2: 1);
  }
  LOBYTE(v2) = v11 != 0;
  sub_140808B00(a1: v20);
  sub_140808B00(a1: &v19);
LABEL_5:
  sub_140808B00(a1: v29);
  v6 = v17;
  if ( v17 == 0 )
    return (unsigned int)v2;
LABEL_8:
  if ( _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
  return (unsigned int)v2;
}
