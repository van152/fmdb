__int64 __fastcall sub_1411D00E0(__int64 a1, __int64 a2, __int64 a3, volatile signed __int32 *a4)
{
  volatile signed __int32 **v4; // rsi
  volatile signed __int32 *v5; // r14
  unsigned int v6; // edi
  int v9; // eax
  __int64 v10; // rcx
  __int64 v11; // rax
  volatile signed __int32 *v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rax
  int v15; // esi
  __int64 v16; // rcx
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 *v19; // rbx
  int v20; // eax
  volatile signed __int32 **v21; // rbx
  volatile signed __int32 *v22; // rax
  volatile signed __int32 *v23; // rcx
  volatile signed __int32 *v24; // rsi
  __int64 v25; // r15
  __int64 v26; // rax
  _QWORD *v27; // rbx
  _QWORD *v28; // rdi
  volatile signed __int32 *v29; // rsi
  volatile signed __int32 *v30; // rcx
  __int64 *v31; // r15
  volatile signed __int32 *v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rax
  volatile signed __int32 **v35; // rax
  __int64 v36; // rcx
  __int64 v37; // rax
  __int64 v38; // rcx
  __int64 v39; // rax
  __int64 v40; // rcx
  __int64 *v41; // rax
  __int64 *v42; // rsi
  volatile signed __int32 *v43; // rsi
  volatile signed __int32 **v44; // rax
  __int64 *v46; // rsi
  int v47; // [rsp+68h] [rbp-18h] BYREF
  __int64 v48; // [rsp+70h] [rbp-10h] BYREF
  int v49; // [rsp+78h] [rbp-8h]
  volatile signed __int32 *v50; // [rsp+80h] [rbp+0h] BYREF
  _QWORD v51[4]; // [rsp+88h] [rbp+8h] BYREF
  volatile signed __int32 **v52; // [rsp+A8h] [rbp+28h] BYREF
  _QWORD v53[8]; // [rsp+B0h] [rbp+30h] BYREF

  v53[2] = -2;
  v5 = a4;
  v6 = a3;
  if ( (a3 & 0xFF000000) != 0x52000000 || BYTE2(a3) != 74 && BYTE2(a3) != 80 )
  {
    if ( a1 != 0 )
      goto LABEL_8;
LABEL_140:
    sub_140F4AEF0(&qword_141B5FDA8, v6, v5);
    goto LABEL_141;
  }
  if ( a1 == 0 )
  {
    if ( (_BYTE)a3 + 10 * BYTE1(a3) == 0xBA && (_BYTE)word_141B60320 != 0 )
    {
      sub_140FE7960(&v47, a4, 0);
      if ( v47 >= 0 )
      {
        sub_1407C9510(&v50);
        v11 = sub_14083D4F0(v10);
        LODWORD(v53[0]) = 1;
        v52 = (volatile signed __int32 **)(v11 + 40);
        sub_140835380(&v50, 1685353593, &v52);
        (*((void (__fastcall **)(volatile signed __int32 **, volatile signed __int32 ***))*v52 + 2))(v52, &v52);
        v12 = v50;
        v13 = v51[0];
        if ( v50 == (volatile signed __int32 *)v51[0] )
          goto LABEL_27;
        while ( *v12 != 1685417577 )
        {
          v12 += 4;
          if ( v12 == (volatile signed __int32 *)v51[0] )
            goto LABEL_27;
        }
        if ( v12 == (volatile signed __int32 *)v51[0] || (v29 = *((volatile signed __int32 **)v12 + 1)) == nullptr )
        {
LABEL_27:
          sub_140835A40(&v50, 1685417577, v5);
        }
        else if ( v29 != v5 )
        {
          (*(void (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)v29 + 16LL))(*(_QWORD *)v29, v29);
          (*(void (__fastcall **)(_QWORD, volatile signed __int32 *, volatile signed __int32 *))(**(_QWORD **)v5 + 24LL))(
            *(_QWORD *)v5,
            v5,
            v29);
        }
        v14 = sub_14083D4F0(v13);
        LODWORD(v53[0]) = 1112566383;
        v52 = (volatile signed __int32 **)(v14 + 56);
        sub_140835380(&v50, 1886549113, &v52);
        (*((void (__fastcall **)(volatile signed __int32 **, volatile signed __int32 ***))*v52 + 2))(v52, &v52);
        v15 = *(_DWORD *)(a2 + 12);
        v17 = sub_14083D4F0(v16);
        LODWORD(v53[0]) = v15;
        v52 = (volatile signed __int32 **)(v17 + 40);
        sub_140835380(&v50, 1853322860, &v52);
        (*((void (__fastcall **)(volatile signed __int32 **, volatile signed __int32 ***))*v52 + 2))(v52, &v52);
        v18 = qword_141B60C30;
        v19 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v18 != 1986359923 )
          {
            v18 += 16;
            if ( v18 == qword_141B60C38 )
              goto LABEL_108;
          }
          if ( v18 == qword_141B60C38 )
            v19 = nullptr;
          else
            v19 = *(__int64 **)(v18 + 8);
        }
LABEL_108:
        v31 = &qword_141B5A4A0;
        if ( v19 == nullptr )
          v19 = &qword_141B5A4A0;
        v32 = v50;
        if ( v50 == (volatile signed __int32 *)v51[0] )
          goto LABEL_113;
        while ( *v32 != 1986359923 )
        {
          v32 += 4;
          if ( v32 == (volatile signed __int32 *)v51[0] )
            goto LABEL_113;
        }
        if ( v32 == (volatile signed __int32 *)v51[0] || (v42 = *((__int64 **)v32 + 1)) == nullptr )
        {
LABEL_113:
          sub_140835A40(&v50, 1986359923, v19);
        }
        else if ( v42 != v19 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v42 + 16LL))(*v42, v42);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v19 + 24LL))(*v19, v19, v42);
        }
        sub_140F47AD0((unsigned int)&qword_141B5FDA8, (unsigned int)&v50, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0);
        sub_1407C9510(&v52);
        v34 = sub_14083D4F0(v33);
        v49 = 1;
        v48 = v34 + 40;
        sub_140835380(&v52, 1685353593, &v48);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v48 + 16LL))(v48, &v48);
        v35 = v52;
        v36 = v53[0];
        if ( v52 == (volatile signed __int32 **)v53[0] )
          goto LABEL_117;
        while ( *(_DWORD *)v35 != 1685417577 )
        {
          v35 += 2;
          if ( v35 == (volatile signed __int32 **)v53[0] )
            goto LABEL_117;
        }
        if ( v35 == (volatile signed __int32 **)v53[0] || (v43 = v35[1]) == nullptr )
        {
LABEL_117:
          sub_140835A40(&v52, 1685417577, v5);
        }
        else if ( v43 != v5 )
        {
          (*(void (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)v43 + 16LL))(*(_QWORD *)v43, v43);
          (*(void (__fastcall **)(_QWORD, volatile signed __int32 *, volatile signed __int32 *))(**(_QWORD **)v5 + 24LL))(
            *(_QWORD *)v5,
            v5,
            v43);
        }
        v37 = sub_14083D4F0(v36);
        v49 = 1112567146;
        v48 = v37 + 56;
        sub_140835380(&v52, 1886549113, &v48);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v48 + 16LL))(v48, &v48);
        v39 = sub_14083D4F0(v38);
        v49 = 5;
        v48 = v39 + 56;
        sub_140835380(&v52, 1853322860, &v48);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v48 + 16LL))(v48, &v48);
        v40 = qword_141B60C30;
        v41 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v40 != 1986359923 )
          {
            v40 += 16;
            if ( v40 == qword_141B60C38 )
              goto LABEL_133;
          }
          if ( v40 == qword_141B60C38 )
            v41 = nullptr;
          else
            v41 = *(__int64 **)(v40 + 8);
        }
LABEL_133:
        if ( v41 != nullptr )
          v31 = v41;
        v44 = v52;
        if ( v52 == (volatile signed __int32 **)v53[0] )
          goto LABEL_138;
        while ( *(_DWORD *)v44 != 1986359923 )
        {
          v44 += 2;
          if ( v44 == (volatile signed __int32 **)v53[0] )
            goto LABEL_138;
        }
        if ( v44 == (volatile signed __int32 **)v53[0] || (v46 = (__int64 *)v44[1]) == nullptr )
        {
LABEL_138:
          sub_140835A40(&v52, 1986359923, v31);
        }
        else if ( v46 != v31 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v46 + 16LL))(*v46, v46);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v31 + 24LL))(*v31, v31, v46);
        }
        v4 = (volatile signed __int32 **)&v52;
        sub_140F47AD0((unsigned int)&qword_141B5FDA8, (unsigned int)&v52, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0);
        sub_140833970(&v52);
        sub_140833970(&v50);
      }
    }
    goto LABEL_140;
  }
  if ( (_BYTE)a3 + 10 * BYTE1(a3) != 16 )
  {
    LOBYTE(v4) = 1;
    if ( (_BYTE)word_141B60320 != 0 )
      return (unsigned int)v4;
  }
LABEL_8:
  LODWORD(v4) = 0;
  if ( (int)a3 > 1315202668 )
  {
    if ( (int)a3 > 1416324912 )
    {
      if ( (int)a3 > 1416326960 )
      {
        switch ( (_DWORD)a3 )
        {
          case 0x546B6F33:
            LOBYTE(a3) = 2;
            break;
          case 0x546B6F32:
            LOBYTE(a3) = 1;
            break;
          case 0x546B6F31:
            a3 = 0;
            break;
          default:
            return (unsigned int)v4;
        }
        LOBYTE(a4) = 1;
      }
      else
      {
        switch ( (_DWORD)a3 )
        {
          case 0x546B6731:
            a3 = 0;
            a4 = nullptr;
            break;
          case 0x546B6732:
            LOBYTE(a3) = 1;
            a4 = nullptr;
            break;
          case 0x546B6733:
            LOBYTE(a3) = 2;
            a4 = nullptr;
            break;
          default:
            return (unsigned int)v4;
        }
      }
      sub_1415EB990(&v50, a2, a3, a4);
      v52 = &v50;
      v53[0] = v51;
      v20 = sub_1411FA5C0(&v52, v5);
    }
    else
    {
      if ( (int)a3 <= 1413703795 )
      {
        if ( (_DWORD)a3 == 1315202669 )
          goto LABEL_76;
        if ( (_DWORD)a3 != 1315992166 )
        {
          if ( (_DWORD)a3 != 1316188262 )
            return (unsigned int)v4;
LABEL_68:
          *(_BYTE *)(a1 + 117) = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)v5 + 64LL))(
                                   *(_QWORD *)v5,
                                   v5);
          goto LABEL_141;
        }
LABEL_37:
        *(_BYTE *)(a1 + 116) = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)v5 + 64LL))(
                                 *(_QWORD *)v5,
                                 v5);
        goto LABEL_141;
      }
      if ( (_DWORD)a3 == 1413703796 )
      {
        v4 = &v50;
        (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, volatile signed __int32 *))(**(_QWORD **)a4 + 128LL))(
          *(_QWORD *)a4,
          &v50,
          a4);
        sub_140809170(a1 + 152, &v50);
LABEL_104:
        v30 = v50;
        if ( v50 != nullptr && _InterlockedDecrement(v50 - 1) == 0 )
          sub_1412EC9A0((__int64)(v30 - 1));
        goto LABEL_141;
      }
      if ( (_DWORD)a3 == 1413705326 )
      {
LABEL_59:
        v4 = &v50;
        (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, volatile signed __int32 *))(**(_QWORD **)a4 + 128LL))(
          *(_QWORD *)a4,
          &v50,
          a4);
        v21 = (volatile signed __int32 **)(a1 + 144);
        if ( v21 != &v50 )
        {
          v22 = *v21;
          v23 = *v21 - 1;
          if ( *v21 == nullptr )
            v23 = nullptr;
          v24 = v50 - 1;
          if ( v50 != nullptr )
          {
            if ( v22 != nullptr && _InterlockedDecrement(v23) == 0 )
              sub_1412EC9A0((__int64)v23);
            *v21 = nullptr;
            _InterlockedIncrement(v24);
            v4 = (volatile signed __int32 **)(v24 + 1);
          }
          else
          {
            if ( v22 != nullptr && _InterlockedDecrement(v23) == 0 )
              sub_1412EC9A0((__int64)v23);
            v4 = nullptr;
          }
          *v21 = (volatile signed __int32 *)v4;
        }
        goto LABEL_104;
      }
      if ( (_DWORD)a3 != 1413706355 )
        return (unsigned int)v4;
      sub_141563FA0(&v50, a2);
      v52 = &v50;
      v53[0] = v51;
      v20 = sub_1411FC540(&v52, v5);
    }
    LODWORD(v4) = v20;
    if ( v51[0] != 0 )
      sub_1407E4890(qword_141ABD470, v51[0], v51[2] - v51[0]);
    return (unsigned int)v4;
  }
  if ( (int)a3 > 1131247712 )
  {
    if ( (int)a3 > 1131570541 )
    {
      if ( (_DWORD)a3 == 1131570542 )
      {
        v52 = (volatile signed __int32 **)a2;
        v53[0] = a2;
        v50 = (volatile signed __int32 *)&v52;
        v51[0] = v53;
        v9 = sub_1411FE490(&v50, a4);
        goto LABEL_80;
      }
      if ( (_DWORD)a3 == 1131572084 )
      {
        LOBYTE(v4) = 1;
        if ( *(_BYTE *)(a2 + 186) == 1 )
        {
          v25 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a2 + 416LL))(a2);
          v26 = *(_QWORD *)(qword_141B5FDB8 + 128);
          v27 = *(_QWORD **)v26;
          v28 = *(_QWORD **)(v26 + 8);
          while ( v27 != v28 )
          {
            if ( *(_QWORD *)(*v27 + 216LL) == v25 )
              sub_140E834A0(*v27, 1131572084, v5);
            ++v27;
          }
        }
        return (unsigned int)v4;
      }
      if ( (_DWORD)a3 != 1315006061 )
        return (unsigned int)v4;
      goto LABEL_70;
    }
    if ( (_DWORD)a3 == 1131247713 )
    {
      *(_DWORD *)(a1 + 112) = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)a4 + 64LL))(
                                *(_QWORD *)a4,
                                a4);
      goto LABEL_141;
    }
    if ( (_DWORD)a3 != 1131309934 )
    {
      if ( (_DWORD)a3 != 1131439730 )
        return (unsigned int)v4;
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)a4 + 8LL))(
             *(_QWORD *)a4,
             a4) == 0 )
        goto LABEL_77;
      goto LABEL_37;
    }
    goto LABEL_59;
  }
  if ( (int)a3 > 1130460259 )
  {
    if ( (_DWORD)a3 == 1130460260 )
    {
      *(_DWORD *)(a1 + 104) = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)a4 + 64LL))(
                                *(_QWORD *)a4,
                                a4);
      goto LABEL_141;
    }
    if ( (_DWORD)a3 != 1130653295 )
    {
      if ( (_DWORD)a3 != 1131245153 )
        return (unsigned int)v4;
      *(_DWORD *)(a1 + 108) = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)a4 + 64LL))(
                                *(_QWORD *)a4,
                                a4);
LABEL_141:
      LOBYTE(v4) = 1;
      return (unsigned int)v4;
    }
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)a4 + 8LL))(
           *(_QWORD *)a4,
           a4) == 0 )
      goto LABEL_77;
LABEL_76:
    *(_BYTE *)(a1 + 118) = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)v5 + 64LL))(
                             *(_QWORD *)v5,
                             v5);
    goto LABEL_141;
  }
  switch ( (_DWORD)a3 )
  {
    case 0x43327066:
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)a4 + 8LL))(
             *(_QWORD *)a4,
             a4) == 0 )
        goto LABEL_77;
      goto LABEL_68;
    case 0x4361666F:
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)a4 + 8LL))(
             *(_QWORD *)a4,
             a4) != 0 )
      {
LABEL_70:
        *(_BYTE *)(a1 + 119) = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 *))(**(_QWORD **)v5 + 64LL))(
                                 *(_QWORD *)v5,
                                 v5);
        goto LABEL_141;
      }
LABEL_77:
      *(_BYTE *)(a1 + 116) = 0;
      goto LABEL_141;
    case 0x43616C74:
      v52 = (volatile signed __int32 **)a2;
      v53[0] = a2;
      v50 = (volatile signed __int32 *)&v52;
      v51[0] = v53;
      v9 = sub_1411FD130(&v50, a4);
LABEL_80:
      LODWORD(v4) = v9;
      break;
    default:
      break;
  }
  return (unsigned int)v4;
}
