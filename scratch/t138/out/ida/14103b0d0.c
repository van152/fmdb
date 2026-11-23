__int64 __fastcall sub_14103B0D0(__int64 a1, volatile signed __int32 **a2)
{
  unsigned __int16 v3; // r14
  volatile signed __int32 *v4; // rbx
  _WORD *v5; // rdi
  volatile signed __int32 *v6; // rcx
  unsigned int v7; // esi
  volatile signed __int32 *v8; // rax
  __int64 v9; // rdi
  __int64 v10; // rsi
  bool v11; // zf
  __int64 v12; // r8
  char *v13; // rdi
  char *v14; // rbx
  __int64 v15; // rax
  char *v16; // rdx
  char i; // r14
  _WORD *v18; // rdi
  unsigned int *v19; // r15
  volatile signed __int32 *v20; // rcx
  __int64 v21; // r8
  char *v22; // rsi
  __int64 v23; // rax
  __int64 v24; // r8
  __int64 v25; // r8
  __int64 v26; // rax
  volatile signed __int32 *v27; // rcx
  char *v28; // r13
  __int64 v29; // r8
  char *v30; // rdi
  unsigned int *v31; // rsi
  __int64 v32; // r8
  char *v33; // rsi
  char *v34; // rbx
  __int64 v35; // r8
  __int64 v36; // rdi
  __int64 v37; // rsi
  __int64 v38; // r8
  char j; // bl
  volatile signed __int32 *v40; // rcx
  char *v41; // rdi
  char *v42; // rdx
  unsigned int v43; // esi
  char *v44; // rdi
  volatile signed __int32 *v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rbx
  unsigned int *v48; // r14
  unsigned int *v49; // rdi
  __int64 v50; // rbx
  __int64 v51; // rbx
  __int64 v52; // rax
  unsigned __int16 v54; // [rsp+38h] [rbp-48h]
  unsigned int v55; // [rsp+40h] [rbp-40h] BYREF
  _BYTE v56[16]; // [rsp+44h] [rbp-3Ch] BYREF
  __int64 v57; // [rsp+54h] [rbp-2Ch]
  __int16 v58; // [rsp+5Ch] [rbp-24h]
  char v59; // [rsp+5Eh] [rbp-22h]
  unsigned int v60; // [rsp+64h] [rbp-1Ch] BYREF
  volatile signed __int32 *v61; // [rsp+68h] [rbp-18h] BYREF
  char *v62; // [rsp+70h] [rbp-10h]
  __int64 v63; // [rsp+78h] [rbp-8h]
  char *v64; // [rsp+80h] [rbp+0h]
  char v65; // [rsp+8Eh] [rbp+Eh] BYREF
  char v66; // [rsp+8Fh] [rbp+Fh] BYREF
  _QWORD v67[8]; // [rsp+90h] [rbp+10h] BYREF

  v67[0] = -2;
  v3 = qword_141B60330;
  if ( (unsigned __int16)qword_141B60330 > 0xDCAu )
  {
    v8 = *a2;
    v61 = v8;
    if ( v8 != nullptr )
      _InterlockedIncrement(v8 + 2);
    LOBYTE(v60) = 0;
    v62 = (char *)&v60;
    v63 = 1;
    v64 = (char *)&v60 + 1;
    if ( v61 != nullptr )
    {
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: &v60,
        a3: 1);
      v62 = nullptr;
      v63 = 0;
      v64 = nullptr;
      if ( (_BYTE)v60 != 0 )
      {
        v9 = sub_14103F110(a1: 176);
        if ( qword_141ABD470 == 0 )
        {
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
            }
          }
          qword_141ABD470 = (__int64)&unk_141B59A68;
        }
        sub_141758A10(a1: v9, a2: 0, a3: 175);
        v10 = *(_QWORD *)(a1 + 96);
        *(_QWORD *)(a1 + 96) = v9;
        if ( v10 != 0 )
        {
          sub_14103EA70(a1: v10);
          sub_14103F010(a1: v10);
          v9 = *(_QWORD *)(a1 + 96);
        }
        if ( v63 != 0 && v61 != nullptr )
          (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
        v64 = nullptr;
        v63 = 0;
        v62 = nullptr;
        if ( (unsigned __int8)sub_141441770(a1: v9, a2: &v61) == 0 )
          goto LABEL_47;
        v66 = 0;
        if ( v64 == &v66 )
        {
          v11 = v63++ == -1;
          v64 = (char *)v67;
          if ( v11 )
            goto LABEL_37;
          goto LABEL_35;
        }
LABEL_31:
        if ( v63 != 0 && v61 != nullptr )
          (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
        v62 = &v66;
        v63 = 1;
        v64 = (char *)v67;
LABEL_35:
        if ( v61 != nullptr )
          (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
LABEL_37:
        v64 = nullptr;
        v63 = 0;
        v62 = nullptr;
        if ( v66 > 0 )
        {
          v54 = v3;
          for ( i = 0; i < v66; ++i )
          {
            v55 = 124518401;
            memset(v56, 255, 13);
            v57 = 0xFFFFFFFFLL;
            v58 = -1;
            v59 = 0;
            sub_14156AF70(a1: &v55, a2: &v61);
            sub_14103AF20(a1: a1 + 104, a2: &v55);
          }
          v3 = v54;
          if ( v63 != 0 && v61 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
        }
        v18 = (_WORD *)(a1 + 128);
        v64 = nullptr;
        v63 = 0;
        v62 = nullptr;
        v19 = &v55;
        (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v61 + 40LL))(
          a1: v61,
          a2: &v55,
          a3: 1);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
          a1: v61,
          a2: a1 + 128,
          a3: 2);
        if ( (unsigned __int8)v55 <= 2u && (*v18 & 0x1FC0) == 0x380 )
          *v18 = *v18 & 0xE03F | 0x3C0;
        v20 = v61;
        if ( *((_DWORD *)v61 + 4) != 0 )
        {
LABEL_47:
          v7 = 0;
LABEL_168:
          if ( v63 != 0 )
          {
            if ( v61 == nullptr )
              return v7;
            (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
          }
          v40 = v61;
          v64 = nullptr;
          v63 = 0;
          v62 = nullptr;
          if ( v61 == nullptr )
            return v7;
          goto LABEL_172;
        }
        v21 = v63;
        if ( v64 == (char *)(a1 + 130) )
        {
          v23 = v63 + 4;
          v63 += 4;
          v64 = (char *)(a1 + 134);
          v22 = (char *)(a1 + 136);
          if ( (unsigned int *)(a1 + 134) == &v55 )
          {
            v63 = v21 + 5;
            v64 = (char *)&v55 + 1;
            if ( v21 == -5 )
            {
              v41 = (char *)(a1 + 140);
              v62 = (char *)(a1 + 140);
              v63 = 9;
              v64 = (char *)(a1 + 149);
              goto LABEL_141;
            }
LABEL_139:
            if ( v61 == nullptr )
            {
              v41 = v22 + 4;
LABEL_143:
              v42 = v22;
              v62 = v22;
              v63 = 4;
              v64 = v41;
              v43 = v3;
              if ( v3 < 0xDDDu )
              {
                v44 = (char *)(a1 + 168);
                v45 = v61;
                v46 = 4;
                if ( v61 == nullptr )
                {
LABEL_148:
                  v62 = v44;
                  v63 = v46 + 28;
                  v64 = (char *)(a1 + 200);
                  if ( (unsigned __int16)qword_141B60330 <= 0xDD8u )
                  {
                    v48 = (unsigned int *)(a1 + 204);
                    if ( v61 != nullptr )
                      (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(
                        a1: v61,
                        a2: v44);
                    v62 = (char *)(a1 + 204);
                    v47 = 4;
                  }
                  else
                  {
                    v47 = v46 + 36;
                    v48 = (unsigned int *)v44;
                  }
                  v63 = v47 + 4;
                  v49 = (unsigned int *)(a1 + 212);
                  v64 = (char *)(a1 + 212);
                  if ( v43 > 0xDDC )
                  {
                    v51 = v47 + 20;
                    v49 = v48;
                  }
                  else
                  {
                    v55 = 0;
                    if ( v49 == &v55 )
                    {
                      v50 = v47 + 8;
                      v19 = v48;
                    }
                    else
                    {
                      if ( v61 != nullptr )
                        (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *))(*(_QWORD *)v61 + 40LL))(
                          a1: v61,
                          a2: v48);
                      v62 = (char *)&v55;
                      v50 = 4;
                    }
                    v63 = v50;
                    v64 = v56;
                    if ( v61 != nullptr )
                      (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v61 + 40LL))(
                        a1: v61,
                        a2: v19,
                        a3: v50);
                    v52 = v55;
                    *(_QWORD *)(a1 + 152) = v55;
                    v62 = (char *)&v55;
                    v63 = 4;
                    v64 = v56;
                    if ( v61 != nullptr )
                    {
                      (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v61 + 40LL))(
                        a1: v61,
                        a2: &v55,
                        a3: 4);
                      v52 = v55;
                    }
                    *(_QWORD *)(a1 + 160) = v52;
                    v62 = (char *)(a1 + 212);
                    v51 = 16;
                  }
                  v63 = v51;
                  v64 = (char *)(a1 + 228);
                  if ( v61 != nullptr )
                    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v61 + 40LL))(
                      a1: v61,
                      a2: v49,
                      a3: v51);
                  v64 = nullptr;
                  v63 = 0;
                  v62 = nullptr;
                  v7 = sub_140EDFB90(a1, a2: &v61);
                  goto LABEL_168;
                }
              }
              else
              {
                v44 = (char *)(a1 + 152);
                v45 = v61;
                v46 = 20;
                if ( v61 == nullptr )
                  goto LABEL_148;
              }
              (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v45 + 40LL))(
                a1: v45,
                a2: v42,
                a3: 4);
              goto LABEL_148;
            }
            (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
            v20 = v61;
            v41 = v22 + 4;
            v62 = v22 + 4;
            v63 = 9;
            v64 = v22 + 13;
            if ( v61 == nullptr )
              goto LABEL_143;
LABEL_141:
            (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v20 + 40LL))(
              a1: v20,
              a2: v41,
              a3: 9);
            goto LABEL_143;
          }
          if ( v21 == -4 )
            goto LABEL_54;
        }
        else
        {
          if ( v63 != 0 )
            (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v61 + 40LL))(
              a1: v61,
              a2: v62,
              a3: v63);
          v62 = (char *)(a1 + 130);
          v63 = 4;
          v64 = (char *)(a1 + 134);
          v22 = (char *)(a1 + 136);
          if ( (unsigned int *)(a1 + 134) == &v55 )
          {
            v24 = 5;
            goto LABEL_138;
          }
          v20 = v61;
          v23 = 4;
          if ( v61 == nullptr )
          {
LABEL_54:
            v62 = (char *)&v55;
            v24 = 1;
LABEL_138:
            v63 = v24;
            v64 = (char *)&v55 + 1;
            goto LABEL_139;
          }
        }
        (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v20 + 40LL))(
          a1: v20,
          a2: v62,
          a3: v23);
        goto LABEL_54;
      }
    }
    else
    {
      v64 = nullptr;
      v63 = 0;
      v62 = nullptr;
    }
    v66 = 0;
    goto LABEL_31;
  }
  v61 = *a2;
  _InterlockedIncrement(v61 + 2);
  v4 = v61;
  v62 = (char *)(a1 + 168);
  v63 = 4;
  v64 = (char *)(a1 + 172);
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
    a1: v61,
    a2: a1 + 168,
    a3: 4);
  v62 = (char *)(a1 + 176);
  v63 = 8;
  v64 = (char *)(a1 + 184);
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(
    a1: v4,
    a2: a1 + 176,
    a3: 8);
  v5 = (_WORD *)(a1 + 128);
  v62 = nullptr;
  v63 = 0;
  v64 = nullptr;
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v4 + 40LL))(
    a1: v4,
    a2: &v55,
    a3: 1);
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
    a1: v61,
    a2: a1 + 128,
    a3: 2);
  if ( (unsigned __int8)v55 <= 2u && (*v5 & 0x1FC0) == 0x380 )
    *v5 = *v5 & 0xE03F | 0x3C0;
  v6 = v61;
  if ( *((_DWORD *)v61 + 4) != 0 )
    goto LABEL_6;
  v12 = v63;
  if ( v64 == (char *)(a1 + 208) )
  {
    v15 = v63 + 4;
    v63 += 4;
    v13 = (char *)(a1 + 212);
    v64 = (char *)(a1 + 212);
    v60 = 0;
    v14 = (char *)&v60;
    if ( (unsigned int *)(a1 + 212) == &v60 )
    {
      v63 = v12 + 8;
      v64 = (char *)&v61;
      if ( v12 == -8 )
      {
        *(_QWORD *)(a1 + 152) = v60;
        v14 = (char *)&v60;
        v62 = (char *)&v60;
        v63 = 4;
        v64 = (char *)&v61;
        goto LABEL_66;
      }
      goto LABEL_65;
    }
    if ( v12 != -4 )
    {
      v16 = v62;
LABEL_58:
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v6 + 40LL))(
        a1: v6,
        a2: v16,
        a3: v15);
    }
LABEL_59:
    v62 = (char *)&v60;
    v25 = 4;
    v14 = v13;
    goto LABEL_64;
  }
  if ( v63 != 0 )
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v61 + 40LL))(
      a1: v61,
      a2: v62,
      a3: v63);
  v62 = (char *)(a1 + 208);
  v63 = 4;
  v13 = (char *)(a1 + 212);
  v64 = (char *)(a1 + 212);
  v60 = 0;
  v14 = (char *)&v60;
  if ( (unsigned int *)(a1 + 212) != &v60 )
  {
    v6 = v61;
    v15 = 4;
    v16 = (char *)(a1 + 208);
    if ( v61 == nullptr )
      goto LABEL_59;
    goto LABEL_58;
  }
  v25 = 8;
LABEL_64:
  v63 = v25;
  v64 = (char *)&v61;
  v6 = v61;
  if ( v61 == nullptr )
  {
    v26 = v60;
    *(_QWORD *)(a1 + 152) = v60;
    v62 = (char *)&v60;
    v63 = 4;
    v64 = (char *)&v61;
    goto LABEL_74;
  }
LABEL_65:
  (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: v62);
  v6 = v61;
  v26 = v60;
  *(_QWORD *)(a1 + 152) = v60;
  v62 = (char *)&v60;
  v63 = 4;
  v64 = (char *)&v61;
  if ( v6 == nullptr )
  {
LABEL_74:
    *(_QWORD *)(a1 + 160) = v26;
    v62 = (char *)(a1 + 130);
    v63 = 4;
    v64 = (char *)(a1 + 134);
LABEL_75:
    v62 = nullptr;
LABEL_76:
    v28 = (char *)(a1 + 220);
    goto LABEL_77;
  }
LABEL_66:
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v6 + 40LL))(
    a1: v6,
    a2: &v60,
    a3: 4);
  v27 = v61;
  *(_QWORD *)(a1 + 160) = v60;
  v62 = (char *)(a1 + 130);
  v63 = 4;
  v64 = (char *)(a1 + 134);
  if ( v27 == nullptr )
    goto LABEL_75;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v27 + 40LL))(
    a1: v27,
    a2: a1 + 130,
    a3: 4);
  v62 = v14;
  v63 = 4;
  v64 = (char *)(a1 + 216);
  if ( v61 == nullptr )
    goto LABEL_75;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v14, a3: 4);
  v62 = (char *)(a1 + 218);
  v63 = 1;
  v64 = (char *)(a1 + 219);
  if ( v61 == nullptr )
    goto LABEL_76;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
    a1: v61,
    a2: a1 + 218,
    a3: 1);
  v62 = (char *)(a1 + 216);
  v63 = 1;
  v64 = (char *)(a1 + 217);
  if ( v61 == nullptr )
    goto LABEL_76;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
    a1: v61,
    a2: a1 + 216,
    a3: 1);
  v62 = (char *)(a1 + 219);
  v63 = 1;
  v28 = (char *)(a1 + 220);
  v64 = (char *)(a1 + 220);
  if ( v61 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
      a1: v61,
      a2: a1 + 219,
      a3: 1);
    v62 = (char *)(a1 + 217);
    v63 = 1;
    v64 = (char *)(a1 + 218);
    if ( v61 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: a1 + 217,
        a3: 1);
  }
LABEL_77:
  v62 = v28;
  v63 = 1;
  v64 = (char *)(a1 + 221);
  v29 = 1;
  if ( (unsigned __int16)qword_141B60330 < 0xDCBu )
  {
    v30 = v28;
  }
  else
  {
    v30 = (char *)(a1 + 226);
    if ( v61 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: v28,
        a3: 1);
    v62 = (char *)(a1 + 226);
    v63 = 2;
    v64 = (char *)(a1 + 228);
    v29 = 2;
  }
  if ( v61 == nullptr )
    goto LABEL_90;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v61 + 40LL))(
    a1: v61,
    a2: v30,
    a3: v29);
  v62 = (char *)(a1 + 188);
  v63 = 4;
  v64 = (char *)(a1 + 192);
  if ( v61 == nullptr )
    goto LABEL_90;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
    a1: v61,
    a2: a1 + 188,
    a3: 4);
  v62 = (char *)(a1 + 184);
  v63 = 4;
  v64 = (char *)(a1 + 188);
  if ( v61 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
      a1: v61,
      a2: a1 + 184,
      a3: 4);
    v62 = (char *)(a1 + 221);
    v63 = 1;
    v64 = (char *)(a1 + 222);
    if ( v61 != nullptr )
    {
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: a1 + 221,
        a3: 1);
      v62 = (char *)(a1 + 192);
      v63 = 8;
      v64 = (char *)(a1 + 200);
      if ( v61 != nullptr )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
          a1: v61,
          a2: a1 + 192,
          a3: 8);
        v62 = (char *)(a1 + 204);
        v63 = 4;
        v64 = (char *)(a1 + 208);
        if ( v61 != nullptr )
        {
          (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
            a1: v61,
            a2: a1 + 204,
            a3: 4);
          v62 = (char *)(a1 + 222);
          v63 = 4;
          v64 = (char *)(a1 + 226);
          if ( v61 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
              a1: v61,
              a2: a1 + 222,
              a3: 4);
        }
      }
    }
  }
  else
  {
LABEL_90:
    v62 = nullptr;
  }
  v62 = (char *)(a1 + 172);
  v63 = 4;
  v64 = (char *)(a1 + 176);
  v31 = &v55;
  if ( (unsigned int *)(a1 + 176) == &v55 )
  {
    v32 = 5;
    v31 = (unsigned int *)(a1 + 172);
  }
  else
  {
    if ( v61 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: a1 + 172,
        a3: 4);
    v62 = (char *)&v55;
    v32 = 1;
  }
  v63 = v32;
  v64 = (char *)&v55 + 1;
  if ( v61 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v31);
    v33 = (char *)(a1 + 140);
    v62 = (char *)(a1 + 140);
    v63 = 9;
    v64 = (char *)(a1 + 149);
    if ( v61 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: a1 + 140,
        a3: 9);
  }
  else
  {
    v33 = (char *)(a1 + 140);
  }
  v62 = (char *)(a1 + 136);
  v63 = 4;
  v64 = v33;
  v66 = 0;
  v34 = &v66;
  if ( v33 == &v66 )
  {
    v35 = 5;
    v34 = (char *)(a1 + 136);
  }
  else
  {
    if ( v61 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: a1 + 136,
        a3: 4);
    v62 = &v66;
    v35 = 1;
  }
  v63 = v35;
  v64 = (char *)v67;
  if ( v61 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v34);
  v64 = nullptr;
  v63 = 0;
  v62 = nullptr;
  if ( v66 == 0 )
  {
    v65 = 0;
    goto LABEL_122;
  }
  v36 = sub_14103F110(a1: 176);
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  sub_141758A10(a1: v36, a2: 0, a3: 175);
  v37 = *(_QWORD *)(a1 + 96);
  *(_QWORD *)(a1 + 96) = v36;
  if ( v37 != 0 )
  {
    sub_14103EA70(a1: v37);
    sub_14103F010(a1: v37);
    v36 = *(_QWORD *)(a1 + 96);
  }
  if ( v63 != 0 && v61 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
  v64 = nullptr;
  v63 = 0;
  v62 = nullptr;
  if ( (unsigned __int8)sub_141441770(a1: v36, a2: &v61) != 0 )
  {
    v65 = 0;
    if ( v64 == &v65 )
    {
      v38 = v63 + 1;
      v63 = v38;
      v64 = &v66;
      if ( v38 == 0 )
      {
LABEL_125:
        v64 = nullptr;
        v63 = 0;
        v62 = nullptr;
        if ( v65 > 0 )
        {
          for ( j = 0; j < v65; ++j )
          {
            v55 = 124518401;
            memset(v56, 255, 13);
            v57 = 0xFFFFFFFFLL;
            v58 = -1;
            v59 = 0;
            sub_14156AF70(a1: &v55, a2: &v61);
            sub_14103AF20(a1: a1 + 104, a2: &v55);
          }
          if ( v63 != 0 && v61 != nullptr )
            (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
        }
        v64 = nullptr;
        v63 = 0;
        v62 = nullptr;
        v7 = sub_140EDFB90(a1, a2: &v61);
        goto LABEL_132;
      }
LABEL_123:
      if ( v61 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v61 + 40LL))(
          a1: v61,
          a2: v62,
          a3: v38);
      goto LABEL_125;
    }
    if ( v63 != 0 && v61 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v61 + 40LL))(
        a1: v61,
        a2: v62,
        a3: v63);
LABEL_122:
    v62 = &v65;
    v63 = 1;
    v64 = &v66;
    v38 = 1;
    goto LABEL_123;
  }
LABEL_6:
  v7 = 0;
LABEL_132:
  if ( v63 != 0 )
  {
    if ( v61 == nullptr )
      return v7;
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62);
  }
  v40 = v61;
  v64 = nullptr;
  v63 = 0;
  v62 = nullptr;
  if ( v61 == nullptr )
    return v7;
LABEL_172:
  if ( _InterlockedDecrement(v40 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v40)(a1: v40, a2: 1);
  return v7;
}
