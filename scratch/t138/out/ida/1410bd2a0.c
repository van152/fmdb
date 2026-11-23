__int64 __fastcall sub_1410BD2A0(__int64 *a1, int a2, int a3, char a4)
{
  _QWORD *v7; // rdi
  int *v8; // rax
  int v9; // r14d
  int v10; // esi
  __int64 v11; // r15
  volatile signed __int32 *v12; // r13
  unsigned int v13; // eax
  __int64 v14; // rdi
  __int64 v15; // rbx
  __int64 v16; // rdx
  _BYTE *v17; // rsi
  __int64 v18; // r15
  volatile signed __int32 *v19; // rcx
  __int64 *v20; // rsi
  volatile signed __int32 *v21; // rcx
  __int64 *v22; // r12
  __int64 v23; // rcx
  _DWORD *v24; // rsi
  _DWORD *v25; // rsi
  _DWORD *v26; // rsi
  int v27; // eax
  __int16 v28; // cx
  char v29; // dl
  __int64 v30; // rbx
  __int64 v31; // rbx
  __int64 v32; // r14
  __int64 v33; // r13
  __int64 v34; // rcx
  int v35; // r15d
  unsigned __int8 v36; // al
  __int64 *v37; // rcx
  __int64 v38; // rdi
  int v39; // eax
  __int64 *v40; // r8
  __int64 v41; // rdi
  __int64 *v42; // rax
  __int64 v43; // rax
  _QWORD *v44; // rcx
  __int64 **v45; // r13
  __int64 *v46; // rax
  volatile signed __int32 *v47; // rcx
  volatile signed __int32 *v48; // rsi
  __int64 v49; // rcx
  __int64 v50; // rcx
  __int64 v51; // rcx
  _BYTE *v52; // rax
  _QWORD *v53; // rdx
  __int64 v54; // rbx
  _QWORD *v55; // rax
  _QWORD *v56; // rax
  __int64 v57; // rax
  _QWORD *v58; // rax
  _QWORD *v59; // rbx
  _QWORD *v60; // rax
  _QWORD *v61; // rax
  _QWORD *v62; // rdx
  _QWORD *v63; // rbx
  _QWORD *v64; // rdi
  __int64 v65; // rbx
  _QWORD *v66; // rdi
  _DWORD *v67; // rcx
  __int64 v68; // rcx
  __int64 v69; // rcx
  __int64 v70; // rcx
  void (__fastcall ***v71)(_QWORD, __int64); // rcx
  __int64 v72; // rcx
  __int64 *v74; // [rsp+48h] [rbp-38h]
  int v75; // [rsp+54h] [rbp-2Ch] BYREF
  __int64 v76; // [rsp+58h] [rbp-28h] BYREF
  __int64 v77; // [rsp+60h] [rbp-20h] BYREF
  __int64 v78; // [rsp+68h] [rbp-18h] BYREF
  __int64 v79; // [rsp+70h] [rbp-10h] BYREF
  _DWORD *v80; // [rsp+78h] [rbp-8h] BYREF
  __int64 v81; // [rsp+80h] [rbp+0h]
  __int16 v82; // [rsp+8Eh] [rbp+Eh] BYREF
  __int64 v83; // [rsp+90h] [rbp+10h] BYREF
  __int64 v84; // [rsp+98h] [rbp+18h]
  __int64 v85; // [rsp+A0h] [rbp+20h]
  _BYTE v86[7]; // [rsp+A8h] [rbp+28h]
  _DWORD *v87; // [rsp+B0h] [rbp+30h] BYREF
  char v88; // [rsp+BFh] [rbp+3Fh] BYREF
  __int64 v89; // [rsp+C0h] [rbp+40h]

  v89 = -2;
  if ( a4 != 0 )
  {
    v7 = (_QWORD *)*a1;
    sub_1410BE140(a1, a2: a1, a3: *(_QWORD *)(*a1 + 8));
    v7[1] = v7;
    *v7 = v7;
    v7[2] = v7;
    a1[1] = 0;
  }
  v78 = 0;
  sub_14080D0E0(a1: &v79, a2: 0x1418E2C24LL);
  LODWORD(v87) = a2;
  sub_1408085A0(a1: &v83, a2: &v87);
  v8 = (int *)v83;
  v81 = v83;
  if ( v83 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v83 - 4));
    v9 = *v8;
  }
  else
  {
    v9 = 0;
  }
  v74 = a1;
  v10 = v9 + 12;
  v11 = sub_1412EC810(a1: 264, a2: (unsigned int)(v9 + 12));
  v12 = (volatile signed __int32 *)v11;
  *(_DWORD *)v11 = 0;
  v13 = 0;
  if ( v9 + 12 <= 0 )
    v10 = 0;
  *(_DWORD *)(v11 + 4) = v10;
  v14 = v11 + 8;
  *(_BYTE *)(v11 + 8) = 0;
  if ( v9 <= 0 )
  {
    v17 = (_BYTE *)(v11 + 8);
    v15 = v81;
    if ( v9 != 0 )
      goto LABEL_14;
  }
  else
  {
    v15 = v81;
    v16 = 0x1419435F1LL;
    if ( v81 != 0 )
      v16 = v81 + 4;
    sub_141758A00(a1: v11 + 8, a2: v16, a3: (unsigned int)v9);
    v17 = (_BYTE *)(v14 + (unsigned int)v9);
  }
  *v17 = 0;
  v13 = v9;
LABEL_14:
  v18 = v11 + 4;
  v19 = (volatile signed __int32 *)(v15 - 4);
  strcpy((char *)(v14 + v13), "person_names");
  if ( v15 != 0 && _InterlockedDecrement(v19) == 0 )
    sub_1412EC9A0(a1: v19);
  _InterlockedIncrement(v12);
  _InterlockedIncrement(v12);
  LODWORD(v20) = a3;
  if ( v78 == v18 )
  {
    v22 = v74;
    if ( _InterlockedDecrement(v12) == 0 )
      sub_1412EC9A0(a1: v12);
  }
  else
  {
    v21 = (volatile signed __int32 *)(v78 - 4);
    if ( v78 == 0 )
      v21 = nullptr;
    v22 = v74;
    if ( v78 != 0 && _InterlockedDecrement(v21) == 0 )
      sub_1412EC9A0(a1: v21);
    v78 = v18;
  }
  if ( _InterlockedDecrement(v12) == 0 )
    sub_1412EC9A0(a1: v12);
  v23 = v83;
  if ( v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 - 4)) == 0 )
    sub_1412EC9A0(a1: v23 - 4);
  v83 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v83,
    a2: (unsigned int)&v87,
    a3: (_DWORD)v20,
    a4: (unsigned int)&v78,
    a5: (__int64)&v79,
    a6: 0,
    a7: 0,
    0);
  if ( v87 == nullptr )
  {
    LODWORD(v20) = 0;
    goto LABEL_152;
  }
  v79 = 0;
  v76 = 0;
  v77 = 0;
  v80 = nullptr;
  sub_140814B10(a1: v87, a2: &v83, a3: &v80);
  if ( (_DWORD)v83 != 0 )
  {
LABEL_33:
    LOBYTE(v20) = v87[4] == 0;
    goto LABEL_137;
  }
  while ( 1 )
  {
    if ( v80 == nullptr || *v80 == 0 )
      goto LABEL_33;
    sub_140814B10(a1: v87, a2: &v83, a3: &v79);
    if ( (_DWORD)v83 != 0 )
      break;
    sub_140814B10(a1: v87, a2: &v83, a3: &v76);
    if ( (_DWORD)v83 != 0 )
      break;
    sub_140814B10(a1: v87, a2: &v83, a3: &v77);
    if ( (_DWORD)v83 != 0 )
      break;
    v24 = v87;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v87 + 40LL))(a1: v87, a2: &v75, a3: 4);
    if ( v24[4] != 0 )
      break;
    v25 = v87;
    (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v87 + 40LL))(a1: v87, a2: &v82, a3: 2);
    if ( v25[4] != 0 )
      break;
    v26 = v87;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v87 + 40LL))(a1: v87, a2: &v88, a3: 1);
    if ( v26[4] != 0 )
      break;
    v27 = v75;
    v28 = v82;
    v29 = v88;
    v30 = v79;
    if ( v79 != 0 )
    {
      v83 = 0;
      _InterlockedIncrement((volatile signed __int32 *)(v79 - 4));
    }
    v83 = v30;
    v31 = v76;
    if ( v76 != 0 )
    {
      v84 = 0;
      _InterlockedIncrement((volatile signed __int32 *)(v76 - 4));
    }
    v84 = v31;
    v32 = v77;
    if ( v77 != 0 )
    {
      v85 = 0;
      _InterlockedIncrement((volatile signed __int32 *)(v77 - 4));
    }
    v85 = v32;
    v86[6] = v29;
    *(_WORD *)&v86[4] = v28;
    *(_DWORD *)v86 = v27;
    v33 = *v22;
    v34 = *(_QWORD *)(*v22 + 8);
    v35 = 0;
    if ( *(_BYTE *)(v34 + 25) != 0 )
    {
      v20 = *(__int64 **)(*v22 + 8);
      if ( *(_BYTE *)(v33 + 25) != 0 )
        goto LABEL_59;
    }
    else
    {
      do
      {
        v20 = (__int64 *)v34;
        v36 = sub_1410C05B0(a1: v34 + 32, a2: &v83);
        v37 = v20 + 2;
        if ( v36 == 0 )
        {
          v33 = (__int64)v20;
          v37 = v20;
        }
        v34 = *v37;
      }
      while ( *(_BYTE *)(v34 + 25) == 0 );
      v35 = v36 ^ 1;
      if ( *(_BYTE *)(v33 + 25) != 0 )
      {
LABEL_59:
        if ( v22[1] == 0x38E38E38E38E38ELL )
          sub_140052D20();
        v38 = *v22;
        v33 = sub_1407E4490(a1: qword_141ABD470, a2: 72);
        *(_QWORD *)(v33 + 32) = v83;
        v83 = 0;
        *(_QWORD *)(v33 + 40) = v84;
        v84 = 0;
        *(_QWORD *)(v33 + 48) = v32;
        v85 = 0;
        v39 = *(_DWORD *)v86;
        *(_DWORD *)(v33 + 59) = *(_DWORD *)&v86[3];
        *(_DWORD *)(v33 + 56) = v39;
        *(_QWORD *)(v33 + 64) = 0;
        *(_QWORD *)v33 = v38;
        *(_QWORD *)(v33 + 8) = v38;
        *(_QWORD *)(v33 + 16) = v38;
        *(_WORD *)(v33 + 24) = 0;
        ++v22[1];
        v40 = (__int64 *)*v22;
        *(_QWORD *)(v33 + 8) = v20;
        if ( v20 == v40 )
        {
          *v20 = v33;
          v20[1] = v33;
          v20[2] = v33;
          v43 = v33;
LABEL_70:
          *(_BYTE *)(v43 + 24) = 1;
          goto LABEL_71;
        }
        v41 = v33 + 8;
        if ( v35 != 0 )
        {
          *v20 = v33;
          v42 = v40;
          if ( v20 == (__int64 *)*v40 )
LABEL_67:
            *v42 = v33;
        }
        else
        {
          v20[2] = v33;
          if ( v20 == (__int64 *)v40[2] )
          {
            v42 = v40 + 2;
            goto LABEL_67;
          }
        }
        v44 = *(_QWORD **)v41;
        if ( *(_BYTE *)(*(_QWORD *)v41 + 24LL) != 0 )
        {
LABEL_69:
          v43 = v40[1];
          goto LABEL_70;
        }
        v52 = v44 + 3;
        v53 = (_QWORD *)v33;
        while ( 2 )
        {
          v20 = (__int64 *)v44[1];
          v54 = *v20;
          if ( v44 == (_QWORD *)*v20 )
          {
            v54 = v20[2];
            if ( *(_BYTE *)(v54 + 24) == 0 )
              goto LABEL_94;
            if ( v53 == (_QWORD *)v44[2] )
            {
              v44[2] = *v53;
              if ( *(_BYTE *)(*v53 + 25LL) == 0 )
              {
                *(_QWORD *)(*v53 + 8LL) = v44;
                v20 = (__int64 *)v44[1];
              }
              v53[1] = v20;
              if ( *(_QWORD **)(*v22 + 8) == v44 )
              {
                v60 = (_QWORD *)(*v22 + 8);
              }
              else
              {
                v59 = (_QWORD *)v44[1];
                v60 = v59 + 2;
                if ( (_QWORD *)*v59 == v44 )
                  v60 = (_QWORD *)v44[1];
              }
              *v60 = v53;
              *v53 = v44;
              v44[1] = v53;
              v56 = v53;
            }
            else
            {
              v56 = v44;
              v44 = v53;
            }
            *((_BYTE *)v56 + 24) = 1;
            *(_BYTE *)(*(_QWORD *)(v44[1] + 8LL) + 24LL) = 0;
            v61 = *(_QWORD **)(v44[1] + 8LL);
            v62 = (_QWORD *)*v61;
            *v61 = *(_QWORD *)(*v61 + 16LL);
            v65 = v62[2];
            if ( *(_BYTE *)(v65 + 25) == 0 )
              *(_QWORD *)(v65 + 8) = v61;
            v62[1] = v61[1];
            if ( *(_QWORD **)(*v22 + 8) == v61 )
            {
              v66 = (_QWORD *)(*v22 + 8);
            }
            else
            {
              v66 = (_QWORD *)(v61[1] + 16LL);
              if ( (_QWORD *)*v66 != v61 )
                v66 = (_QWORD *)v61[1];
            }
            *v66 = v62;
            v62[2] = v61;
LABEL_135:
            v61[1] = v62;
          }
          else
          {
            if ( *(_BYTE *)(v54 + 24) != 0 )
            {
              if ( v53 == (_QWORD *)*v44 )
              {
                *v44 = v53[2];
                v57 = v53[2];
                if ( *(_BYTE *)(v57 + 25) == 0 )
                {
                  *(_QWORD *)(v57 + 8) = v44;
                  v20 = (__int64 *)v44[1];
                }
                v53[1] = v20;
                if ( *(_QWORD **)(*v22 + 8) == v44 )
                {
                  v58 = (_QWORD *)(*v22 + 8);
                }
                else
                {
                  v58 = (_QWORD *)(v44[1] + 16LL);
                  if ( (_QWORD *)*v58 != v44 )
                    v58 = (_QWORD *)v44[1];
                }
                *v58 = v53;
                v53[2] = v44;
                v44[1] = v53;
                v55 = v53;
              }
              else
              {
                v55 = v44;
                v44 = v53;
              }
              *((_BYTE *)v55 + 24) = 1;
              *(_BYTE *)(*(_QWORD *)(v44[1] + 8LL) + 24LL) = 0;
              v61 = *(_QWORD **)(v44[1] + 8LL);
              v62 = (_QWORD *)v61[2];
              v61[2] = *v62;
              if ( *(_BYTE *)(*v62 + 25LL) == 0 )
                *(_QWORD *)(*v62 + 8LL) = v61;
              v62[1] = v61[1];
              if ( *(_QWORD **)(*v22 + 8) == v61 )
              {
                v64 = (_QWORD *)(*v22 + 8);
              }
              else
              {
                v63 = (_QWORD *)v61[1];
                v64 = v63 + 2;
                if ( (_QWORD *)*v63 == v61 )
                  v64 = (_QWORD *)v61[1];
              }
              *v64 = v62;
              *v62 = v61;
              goto LABEL_135;
            }
LABEL_94:
            *v52 = 1;
            *(_BYTE *)(v54 + 24) = 1;
            *(_BYTE *)(*(_QWORD *)(*(_QWORD *)v41 + 8LL) + 24LL) = 0;
            v44 = *(_QWORD **)(*(_QWORD *)v41 + 8LL);
          }
          v53 = v44;
          v41 = (__int64)(v44 + 1);
          v44 = (_QWORD *)v44[1];
          v52 = v44 + 3;
          if ( *((_BYTE *)v44 + 24) != 0 )
            goto LABEL_69;
          continue;
        }
      }
    }
    if ( (unsigned __int8)sub_1410C05B0(a1: &v83, a2: v33 + 32) != 0 )
      goto LABEL_59;
LABEL_71:
    v45 = (__int64 **)(v33 + 64);
    if ( v45 != (__int64 **)&v80 )
    {
      v46 = *v45;
      v47 = (volatile signed __int32 *)*v45 - 1;
      if ( *v45 == nullptr )
        v47 = nullptr;
      v48 = v80 - 1;
      if ( v80 != nullptr )
      {
        if ( v46 != nullptr && _InterlockedDecrement(v47) == 0 )
          sub_1412EC9A0(a1: v47);
        *v45 = nullptr;
        _InterlockedIncrement(v48);
        v20 = (__int64 *)(v48 + 1);
      }
      else
      {
        if ( v46 != nullptr && _InterlockedDecrement(v47) == 0 )
          sub_1412EC9A0(a1: v47);
        v20 = nullptr;
      }
      *v45 = v20;
    }
    v49 = v85;
    if ( v85 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v85 - 4)) == 0 )
      sub_1412EC9A0(a1: v49 - 4);
    v50 = v84;
    if ( v84 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v84 - 4)) == 0 )
      sub_1412EC9A0(a1: v50 - 4);
    v51 = v83;
    if ( v83 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v83 - 4)) == 0 )
      sub_1412EC9A0(a1: v51 - 4);
    sub_140814B10(a1: v87, a2: &v83, a3: &v80);
    if ( (_DWORD)v83 != 0 )
      goto LABEL_33;
  }
  LODWORD(v20) = 0;
LABEL_137:
  v67 = v80;
  if ( v80 != nullptr && _InterlockedDecrement(v80 - 1) == 0 )
    sub_1412EC9A0(a1: v67 - 1);
  v68 = v77;
  if ( v77 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v77 - 4)) == 0 )
    sub_1412EC9A0(a1: v68 - 4);
  v69 = v76;
  if ( v76 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v76 - 4)) == 0 )
    sub_1412EC9A0(a1: v69 - 4);
  v70 = v79;
  if ( v79 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v79 - 4)) == 0 )
    sub_1412EC9A0(a1: v70 - 4);
  v71 = (void (__fastcall ***)(_QWORD, __int64))v87;
  if ( v87 != nullptr && _InterlockedDecrement(v87 + 2) == 0 )
    (**v71)(a1: v71, a2: 1);
LABEL_152:
  v72 = v78;
  if ( v78 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v78 - 4)) == 0 )
    sub_1412EC9A0(a1: v72 - 4);
  return (unsigned int)v20;
}
