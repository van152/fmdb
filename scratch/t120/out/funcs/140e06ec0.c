__int64 __fastcall sub_140E06EC0(__int64 a1, __int64 *a2, char a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
{
  char *v8; // rdi
  __int64 v9; // rbx
  char v11; // r15
  __int64 v12; // rax
  char *v13; // rbx
  char *v14; // r15
  __int64 v15; // rax
  __int64 v16; // rbx
  __int64 v17; // rsi
  __int64 v18; // r8
  _DWORD *v19; // rdi
  _DWORD *v20; // rdi
  _DWORD *v21; // rdi
  _DWORD *v22; // rdi
  char *v23; // rdi
  __int64 v24; // r8
  bool v25; // zf
  __int64 v26; // rax
  __int64 v27; // rsi
  __int64 v28; // rbx
  __int64 v29; // r8
  char *v30; // rdi
  unsigned __int64 v31; // rax
  unsigned __int8 v32; // al
  __int64 v33; // rdi
  char *v34; // rdi
  __int64 v35; // rdi
  __int64 v36; // r8
  __int64 v37; // r8
  __int64 v38; // r8
  _QWORD *v39; // rdi
  _DWORD *v40; // rbx
  __int64 v41; // r8
  __int64 v42; // rdi
  __int64 v43; // rdi
  __int64 v44; // r8
  __int64 v45; // rdi
  __int64 v46; // r8
  __int64 v47; // rdx
  __int64 v48; // rdx
  __int64 v49; // rdi
  __int64 v50; // r8
  char i; // r15
  __int64 v52; // r8
  __int64 v53; // rbx
  __int64 v54; // r8
  __int64 v55; // rdi
  char *v56; // rdi
  __int64 v57; // r8
  __int64 v58; // r14
  int v59; // ebx
  int v60; // ebx
  int v61; // ecx
  __int64 v62; // rax
  void (__fastcall ***v63)(_QWORD, __int64); // rcx
  int v65; // [rsp+30h] [rbp-50h]
  char *v66; // [rsp+40h] [rbp-40h]
  char *v67; // [rsp+58h] [rbp-28h]
  char *v69; // [rsp+68h] [rbp-18h]
  __int64 v70; // [rsp+70h] [rbp-10h]
  char v71; // [rsp+7Fh] [rbp-1h]
  __int64 v72; // [rsp+80h] [rbp+0h] BYREF
  char v73; // [rsp+8Dh] [rbp+Dh] BYREF
  char v74; // [rsp+8Eh] [rbp+Eh] BYREF
  char v75; // [rsp+8Fh] [rbp+Fh] BYREF
  _DWORD *v76; // [rsp+90h] [rbp+10h] BYREF
  char *v77; // [rsp+98h] [rbp+18h]
  __int64 v78; // [rsp+A0h] [rbp+20h]
  char *v79; // [rsp+A8h] [rbp+28h]
  __int64 v80; // [rsp+B0h] [rbp+30h]

  v80 = -2;
  v9 = a4;
  v11 = a7;
  v12 = *a2;
  v76 = (_DWORD *)v12;
  if ( v12 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v12 + 8));
  v70 = a1 - 632;
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( a7 == 0 )
    goto LABEL_191;
  v71 = a3;
  v77 = (char *)(a1 - 126);
  v78 = 10;
  v66 = (char *)(a1 - 116);
  v79 = (char *)(a1 - 116);
  if ( v76 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 126, a3: 10);
    v77 = (char *)(a1 - 19);
    v78 = 1;
    v13 = (char *)(a1 - 18);
    v79 = (char *)(a1 - 18);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 19, a3: 1);
  }
  else
  {
    v13 = (char *)(a1 - 18);
  }
  v77 = (char *)(a1 - 23);
  v78 = 4;
  v79 = (char *)(a1 - 19);
  if ( v76 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 23, a3: 4);
    v77 = v13;
    v78 = 2;
    v14 = (char *)(a1 - 16);
    v79 = (char *)(a1 - 16);
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v13, a3: 2);
  }
  else
  {
    v14 = (char *)(a1 - 16);
  }
  v77 = (char *)(a1 - 336);
  v78 = 4;
  v79 = (char *)(a1 - 332);
  v15 = (HIBYTE(qword_141B6034C) != 0) & (unsigned __int8)(byte_141B5FC2C == 0);
  v16 = 4 * v15 + 4;
  v17 = 4 * v15 - 324;
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 336, a3: 4);
  v77 = (char *)(a1 - 328);
  v78 = v16;
  v79 = (char *)(a1 + v17);
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v16);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 112, a3: 69);
  if ( v76[4] != 0 )
    goto LABEL_46;
  v67 = v14;
  v77 = (char *)(a1 - 168);
  v78 = 4;
  v79 = (char *)(a1 - 164);
  if ( v76 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: 4);
    v77 = (char *)(a1 - 25);
    v78 = 1;
    v69 = (char *)(a1 - 24);
    v79 = (char *)(a1 - 24);
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 25, a3: 1);
  }
  else
  {
    v69 = (char *)(a1 - 24);
  }
  v77 = (char *)(a1 - 140);
  v78 = 4;
  v79 = (char *)(a1 - 136);
  v18 = 14;
  if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDF0u )
  {
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v77 = (char *)(a1 - 132);
    v18 = 6;
  }
  v78 = v18;
  v79 = (char *)(a1 - 126);
  if ( v76 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v77 = v66;
    v78 = 4;
    v79 = (char *)(a1 - 112);
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v66, a3: 4);
  }
  v77 = (char *)(a1 - 29);
  v78 = 4;
  v79 = (char *)(a1 - 25);
  v19 = v76;
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 29, a3: 4);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( *(_BYTE *)(a1 - 27) == 0 )
  {
    *(_BYTE *)(a1 - 27) = *(_BYTE *)(a1 - 120);
    if ( *(_BYTE *)(a1 - 26) != 0 )
      goto LABEL_28;
LABEL_41:
    *(_BYTE *)(a1 - 26) = *(_BYTE *)(a1 - 118);
    goto LABEL_28;
  }
  if ( *(_BYTE *)(a1 - 26) == 0 )
    goto LABEL_41;
LABEL_28:
  if ( v78 != 0 && v19 != nullptr )
    (*(void (__fastcall **)(_DWORD *, _QWORD))(*(_QWORD *)v19 + 40LL))(a1: v19, a2: 0);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v19 + 40LL))(a1: v19, a2: &v72, a3: 1);
  if ( v19[4] != 0 )
    goto LABEL_46;
  v20 = v76;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 300, a3: 2);
  if ( v20[4] != 0 )
    goto LABEL_46;
  v21 = v76;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 298, a3: 2);
  if ( v21[4] != 0 )
    goto LABEL_46;
  v22 = v76;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 - 304, a3: 4);
  if ( v22[4] != 0 )
    goto LABEL_46;
  if ( v79 == (char *)(a1 - 144) )
  {
    v25 = v78 == -4;
    v24 = v78 + 4;
    v78 += 4;
    v79 = (char *)(a1 - 140);
    v23 = v69;
    if ( v25 )
      goto LABEL_45;
  }
  else
  {
    v23 = v69;
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = (char *)(a1 - 144);
    v78 = 4;
    v79 = (char *)(a1 - 140);
    v24 = 4;
  }
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v24);
LABEL_45:
  v77 = v23;
  v78 = 1;
  v79 = (char *)(a1 - 23);
  if ( *(_BYTE *)(a1 - 43) != 0 )
    goto LABEL_46;
  LODWORD(v72) = 0;
  if ( (__int64 *)(a1 - 23) == &v72 )
  {
    v26 = 5;
  }
  else
  {
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v23, a3: 1);
    v77 = (char *)&v72;
    v26 = 4;
  }
  v78 = v26;
  v79 = (char *)&v72 + 4;
  sub_1412E70A0(a1: &v76);
  v27 = (unsigned int)v72;
  if ( (_DWORD)v72 != 0 )
  {
    if ( qword_141AA7808 <= (unsigned __int64)(unsigned int)v72 )
    {
LABEL_176:
      LODWORD(v8) = 0;
      goto LABEL_211;
    }
    v28 = 0;
    do
    {
      v31 = *(unsigned __int8 *)(a1 - 43);
      if ( v31 > 0xB )
      {
        *(_BYTE *)(a1 + *(unsigned __int8 *)(a1 - 30) - 42) = 0;
        v32 = *(_BYTE *)(a1 - 30) + 1;
        if ( v32 >= 0xCu )
          v32 = 0;
        *(_BYTE *)(a1 - 30) = v32;
      }
      else
      {
        *(_BYTE *)(a1 + v31 - 42) = 0;
        *(_BYTE *)(a1 - 43) = v31 + 1;
        v32 = *(_BYTE *)(a1 - 30);
      }
      v33 = v28 + v32 - 12;
      if ( v28 + (unsigned __int64)v32 < 0xC )
        v33 = v28 + v32;
      v34 = (char *)(a1 - 42 + v33);
      if ( v79 == v34 )
      {
        v29 = v78 + 1;
      }
      else
      {
        if ( v78 != 0 && v76 != nullptr )
          (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
        v77 = v34;
        v29 = 1;
      }
      v78 = v29;
      v30 = v34 + 1;
      v79 = v30;
      ++v28;
    }
    while ( v27 != v28 );
  }
  else
  {
    v30 = v79;
  }
  if ( v30 == (char *)(a1 - 164) )
  {
    v35 = a1 - 264;
    v25 = v78 == -4;
    v36 = v78 + 4;
    v78 += 4;
    v79 = (char *)(a1 - 160);
    if ( v25 )
      goto LABEL_78;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = (char *)(a1 - 164);
    v78 = 4;
    v79 = (char *)(a1 - 160);
    v35 = a1 - 264;
    v36 = 4;
  }
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v36);
LABEL_78:
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( (unsigned __int8)sub_14145F800(a1: v35, a2: &v76) == 0 )
    goto LABEL_46;
  if ( v78 != 0 && v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  sub_140814B10(a1: v76, a2: &v72, a3: a1 - 392);
  if ( (_DWORD)v72 != 0 )
    goto LABEL_46;
  if ( v79 == (char *)(a1 - 156) )
  {
    v37 = v78 + 4;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = (char *)(a1 - 156);
    v37 = 4;
  }
  v78 = v37 + 8;
  v79 = (char *)(a1 - 144);
  if ( (char *)(a1 - 144) == &v75 )
  {
    v38 = v37 + 9;
  }
  else
  {
    if ( v37 != -8 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v37 + 8);
    v77 = &v75;
    v38 = 1;
  }
  v78 = v38;
  v79 = (char *)&v76;
  sub_1412E70A0(a1: &v76);
  if ( v75 != 0 )
  {
    v39 = (_QWORD *)sub_140E07FB0();
    *v39 = 0;
    v39[1] = 0;
    v39[2] = 0;
    *(_QWORD *)((char *)v39 + 22) = 0;
    *(_QWORD *)(a1 - 360) = v39;
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    v40 = v76;
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v39, a3: 30);
    if ( v40[4] != 0 )
      goto LABEL_46;
  }
  if ( v79 == &v75 )
  {
    v41 = v78 + 1;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = &v75;
    v41 = 1;
  }
  v78 = v41;
  v79 = (char *)&v76;
  sub_1412E70A0(a1: &v76);
  if ( v75 != 0 )
  {
    v42 = sub_140E41310(a1: 104);
    sub_14146A0F0(a1: v42);
    v72 = v42;
    sub_140E08060(a1: a1 - 384, a2: &v72);
    sub_140E06E90(a1: &v72);
    v43 = *(_QWORD *)(a1 - 384);
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    if ( (unsigned __int8)sub_14146AD40(a1: v43, a2: &v76, a3: a4) == 0 )
      goto LABEL_46;
    sub_140E080A0(a1: v70);
  }
  if ( v79 == &v75 )
  {
    v44 = v78 + 1;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = &v75;
    v44 = 1;
  }
  v78 = v44;
  v79 = (char *)&v76;
  sub_1412E70A0(a1: &v76);
  if ( v75 != 0 )
  {
    v45 = sub_140E08120(a1: 56);
    sub_14144AD20(a1: v45);
    *(_QWORD *)(a1 - 400) = v45;
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    if ( (unsigned __int8)sub_14144AD70(a1: v45, a2: &v76) == 0 )
      goto LABEL_46;
  }
  if ( v79 == &v75 )
  {
    v46 = v78 + 1;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = &v75;
    v46 = 1;
  }
  v78 = v46;
  v79 = (char *)&v76;
  sub_1412E70A0(a1: &v76);
  if ( v75 != 0 )
  {
    sub_140E081D0(a1: &v72);
    if ( (__int64 *)(a1 - 344) != &v72 )
    {
      v48 = v72;
      v72 = 0;
      sub_140E40630(a1: a1 - 344, a2: v48);
    }
    sub_140E08430(a1: &v72);
    v49 = *(_QWORD *)(a1 - 344);
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    if ( (unsigned __int8)sub_14146D370(a1: v49, a2: &v76) == 0 )
    {
LABEL_46:
      LODWORD(v8) = 0;
      goto LABEL_211;
    }
  }
  if ( v79 != &v74 )
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = &v74;
    v78 = 1;
    v79 = &v75;
    v50 = 1;
    goto LABEL_142;
  }
  v50 = v78 + 1;
  v78 = v50;
  v79 = &v75;
  if ( v50 != 0 )
  {
LABEL_142:
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v50);
  }
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( v74 <= 0 )
  {
LABEL_162:
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v77 = (char *)&v72;
    v78 = 1;
    v79 = (char *)&v72 + 1;
    v54 = 1;
LABEL_166:
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v54);
    goto LABEL_168;
  }
  for ( i = 0; i < v74; ++i )
  {
    if ( v79 == &v73 )
    {
      v52 = v78 + 1;
      v78 = v52;
      v79 = &v74;
      if ( v52 == 0 )
        goto LABEL_155;
    }
    else
    {
      if ( v78 != 0 && v76 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
      v77 = &v73;
      v78 = 1;
      v79 = &v74;
      v52 = 1;
    }
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v52);
LABEL_155:
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    if ( v73 != -1 )
    {
      v53 = sub_1413C40A0();
      v72 = v53;
      if ( v78 != 0 && v76 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
      v79 = nullptr;
      v78 = 0;
      v77 = nullptr;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, _DWORD **))(*(_QWORD *)v53 + 8LL))(a1: v53, a2: &v76) == 0 )
        goto LABEL_176;
      sub_14087F540(a1: a1 - 616, a2: &v72);
    }
  }
  if ( v79 != (char *)&v72 )
    goto LABEL_162;
  v54 = v78 + 1;
  v25 = v78++ == -1;
  v79 = (char *)&v72 + 1;
  if ( !v25 )
    goto LABEL_166;
LABEL_168:
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( (_BYTE)v72 == 0 )
  {
    v56 = (char *)(a1 - 320);
    goto LABEL_178;
  }
  v55 = sub_140E08640(a1: v70, a2: v47, a3: v54);
  if ( v78 != 0 && v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( (unsigned __int8)sub_140E06080(a1: v55, a2: &v76) == 0 )
    goto LABEL_176;
  v56 = (char *)(a1 - 320);
  if ( v79 == (char *)(a1 - 320) )
  {
    v8 = (char *)(a1 - 312);
    v25 = v78 == -4;
    v78 += 4;
    v79 = (char *)(a1 - 316);
    if ( v25 )
      goto LABEL_184;
    goto LABEL_182;
  }
LABEL_178:
  if ( v78 != 0 && v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
  v77 = v56;
  v78 = 4;
  v79 = (char *)(a1 - 316);
  v8 = (char *)(a1 - 312);
LABEL_182:
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
LABEL_184:
  v77 = v8;
  v78 = 4;
  v79 = (char *)(a1 - 308);
  sub_14145D260(a1: a1 - 296, a2: &v76);
  if ( v79 == v67 )
  {
    v57 = v78 + 4;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = v67;
    v57 = 4;
  }
  v78 = v57;
  v79 = (char *)(a1 - 12);
  v9 = a4;
  v11 = a7;
  a3 = v71;
LABEL_191:
  if ( a3 == 0 )
    goto LABEL_222;
  if ( v78 != 0 && v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  LODWORD(v8) = 0;
  if ( (unsigned __int8)sub_140DD8520(
                          a1: *(_DWORD *)(*(_QWORD *)(a1 - 624) + 8LL) + (int)v70 + 344,
                          a2: (unsigned int)&v76,
                          a3: 0,
                          a4: v9,
                          a5,
                          a6,
                          a7: v11,
                          a8) != 0 )
  {
    v58 = v9;
    v59 = *(_DWORD *)(*(_QWORD *)(a1 - 624) + 8LL) + v70 + 128;
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    LODWORD(v8) = 0;
    if ( (unsigned __int8)sub_140DFB5C0(a1: v59, a2: (unsigned int)&v76, a3: 0, a4: v58, a5, a6, a7: v11, a8) != 0 )
    {
      v60 = *(_DWORD *)(*(_QWORD *)(a1 - 624) + 4LL) + v70 + 8;
      if ( v78 != 0 && v76 != nullptr )
        (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
      v79 = nullptr;
      v78 = 0;
      v77 = nullptr;
      LOBYTE(v65) = v11;
      LODWORD(v8) = 0;
      v61 = v60;
      v9 = v58;
      if ( (unsigned __int8)sub_141084540(a1: v61, a2: (unsigned int)&v76, a3: 0, a4: v58, a5, a6, a7: v65, a8) != 0 )
      {
LABEL_222:
        if ( *(unsigned __int16 *)(v9 + 1416) <= 0xDE4u )
        {
          v62 = *(_QWORD *)(a1 - 624);
          if ( (*(_BYTE *)(a1 + *(int *)(v62 + 4) - 596) & 2) != 0 )
          {
            *(_BYTE *)(a1 - 186) |= 0x40u;
            *(_QWORD *)(a1 + *(int *)(v62 + 4) - 600) &= ~0x200000000uLL;
          }
        }
        if ( v78 != 0 && v76 != nullptr )
          (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
        v79 = nullptr;
        v78 = 0;
        v77 = nullptr;
        LOBYTE(v8) = v76[4] == 0;
      }
    }
  }
LABEL_211:
  if ( v78 != 0 )
  {
    if ( v76 != nullptr )
    {
      (*(void (__fastcall **)(_DWORD *, char *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
      goto LABEL_214;
    }
  }
  else
  {
LABEL_214:
    v63 = (void (__fastcall ***)(_QWORD, __int64))v76;
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    if ( v76 != nullptr && _InterlockedDecrement(v76 + 2) == 0 )
      (**v63)(a1: v63, a2: 1);
  }
  return (unsigned int)v8;
}
