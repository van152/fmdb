__int64 __fastcall sub_140E4CC40(__int64 a1, __int64 a2, unsigned int *a3)
{
  __int64 *v3; // rbx
  char v6; // al
  char v7; // cl
  __int64 v8; // rdx
  volatile signed __int32 **v9; // rsi
  char v10; // al
  char v11; // cl
  volatile signed __int32 *v13; // rax
  volatile signed __int32 *v14; // rcx
  volatile signed __int32 *v15; // rdi
  volatile signed __int32 *v16; // rdi
  __int64 v17; // rcx
  unsigned int v18; // eax
  unsigned int v19; // eax
  __int64 v20; // rax
  int v21; // esi
  __int64 v22; // rax
  __int64 v23; // rax
  int v24; // edi
  __int64 v25; // rax
  __int64 v26; // [rsp+28h] [rbp-38h] BYREF
  _QWORD v27[3]; // [rsp+30h] [rbp-30h] BYREF
  __int64 *v28; // [rsp+48h] [rbp-18h] BYREF
  _QWORD *v29; // [rsp+50h] [rbp-10h]
  __int64 v30; // [rsp+58h] [rbp-8h]

  v30 = -2;
  if ( (int)a2 <= 1096249454 )
  {
    if ( (int)a2 > 1096246894 )
    {
      if ( (int)a2 > 1096248928 )
      {
        if ( (int)a2 > 1096248943 )
        {
          if ( (_DWORD)a2 == 1096248944 )
          {
            *(_BYTE *)(a1 + 139) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            goto LABEL_122;
          }
          if ( (_DWORD)a2 == 1096249200 )
          {
            v6 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
            v7 = *(_BYTE *)(a1 + 141);
            if ( v6 != 0 )
              *(_BYTE *)(a1 + 141) = v7 | 2;
            else
              *(_BYTE *)(a1 + 141) = v7 & 0xFD;
            goto LABEL_122;
          }
        }
        else
        {
          if ( (_DWORD)a2 == 1096248929 )
          {
            v3 = &v26;
            (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 128LL))(
              *(_QWORD *)a3,
              &v26,
              a3);
            v9 = (volatile signed __int32 **)(a1 + 48);
LABEL_92:
            if ( v9 != (volatile signed __int32 **)&v26 )
            {
              v8 = v26;
              v13 = *v9;
              v14 = *v9 - 1;
              if ( *v9 == nullptr )
                v14 = nullptr;
              v15 = (volatile signed __int32 *)(v26 - 4);
              if ( v26 != 0 )
              {
                if ( v13 != nullptr && _InterlockedDecrement(v14) == 0 )
                  sub_1412EC9A0(v14, v8);
                *v9 = nullptr;
                _InterlockedIncrement(v15);
                v16 = v15 + 1;
              }
              else
              {
                if ( v13 != nullptr && _InterlockedDecrement(v14) == 0 )
                  sub_1412EC9A0(v14, 0);
                v16 = nullptr;
              }
              *v9 = v16;
            }
            v17 = v26;
            if ( v26 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 - 4)) == 0 )
              sub_1412EC9A0(v17 - 4, v8);
            goto LABEL_122;
          }
          if ( (_DWORD)a2 == 1096248937 )
          {
            v3 = (__int64 *)qword_141B5FDD0;
            sub_140FE7960(&v26, a3, 1315856756);
            *(_QWORD *)(a1 + 96) = sub_14002F670(v3, &v26);
            goto LABEL_122;
          }
        }
      }
      else if ( (int)a2 > 1096248678 )
      {
        if ( (_DWORD)a2 == 1096248679 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_BYTE *)(a1 + 147) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_BYTE *)(a1 + 147) = 0;
          goto LABEL_122;
        }
        if ( (_DWORD)a2 == 1096248681 )
        {
          v3 = (__int64 *)qword_141B5FDC0;
          sub_140FE7960(&v26, a3, 1668246896);
          *(_QWORD *)(a1 + 88) = sub_140F7A940(v3, &v26);
          goto LABEL_122;
        }
      }
      else
      {
        if ( (_DWORD)a2 == 1096246895 )
        {
          *(_BYTE *)(a1 + 142) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
          goto LABEL_122;
        }
        if ( (_DWORD)a2 == 1096248673 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_BYTE *)(a1 + 144) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_BYTE *)(a1 + 144) = 0;
          goto LABEL_122;
        }
      }
      return sub_140FE2700(a1, a2, a3);
    }
    if ( (int)a2 > 1096246120 )
    {
      if ( (int)a2 > 1096246385 )
      {
        if ( (_DWORD)a2 == 1096246386 )
        {
          *(_BYTE *)(a1 + 130) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
          goto LABEL_122;
        }
        if ( (_DWORD)a2 == 1096246883 )
        {
          sub_140FE3B40(&v26, a3);
          *(_DWORD *)(a1 + 24) = v26;
          goto LABEL_122;
        }
      }
      else
      {
        if ( (_DWORD)a2 == 1096246121 )
        {
          v3 = (__int64 *)qword_141B5FDC8;
          sub_140FE7960(&v26, a3, 1668247156);
          *(_QWORD *)(a1 + 80) = sub_140FA3700(v3, &v26);
          goto LABEL_122;
        }
        if ( (_DWORD)a2 == 1096246369 )
        {
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B5C8D0);
            if ( dword_141B5C8D0 == -1 )
            {
              sub_140DBC9B0(&qword_141B5C8A0);
              sub_141751048(sub_140DBCA10);
              sub_141750EA0(&dword_141B5C8D0);
            }
          }
          if ( *(__int64 **)a3 == &qword_141B5C8A0 )
          {
            v18 = a3[2];
            WORD1(v28) = v18 >> 17;
            LOWORD(v28) = (v18 >> 8) & 0x1FF | ((_WORD)v18 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(
                      *(_QWORD *)a3,
                      a3) == 27 )
          {
            v3 = &v26;
            (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 160LL))(
              *(_QWORD *)a3,
              &v26,
              a3);
            sub_1413CA830(&v28, &v26);
          }
          else
          {
            LODWORD(v28) = 124518401;
          }
          *(_DWORD *)(a1 + 72) = (_DWORD)v28;
          goto LABEL_122;
        }
      }
      return sub_140FE2700(a1, a2, a3);
    }
    if ( (int)a2 > 1096245858 )
    {
      if ( (_DWORD)a2 == 1096245859 )
      {
        sub_140FE3B40(&v26, a3);
        *(_DWORD *)(a1 + 28) = v26;
        goto LABEL_122;
      }
      if ( (_DWORD)a2 == 1096245874 )
      {
        *(_BYTE *)(a1 + 131) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                 *(_QWORD *)a3,
                                 a3);
        goto LABEL_122;
      }
      return sub_140FE2700(a1, a2, a3);
    }
    if ( (_DWORD)a2 == 1096245604 )
    {
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          sub_140DBC9B0(&qword_141B5C8A0);
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      if ( *(__int64 **)a3 == &qword_141B5C8A0 )
      {
        v19 = a3[2];
        WORD1(v28) = v19 >> 17;
        LOWORD(v28) = (v19 >> 8) & 0x1FF | ((_WORD)v19 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
      {
        v3 = &v26;
        (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, &v26, a3);
        sub_1413CA830(&v28, &v26);
      }
      else
      {
        LODWORD(v28) = 124518401;
      }
      *(_DWORD *)(a1 + 76) = (_DWORD)v28;
      goto LABEL_122;
    }
    if ( (_DWORD)a2 != 1096245616 )
      return sub_140FE2700(a1, a2, a3);
    *(_BYTE *)(a1 + 136) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                             *(_QWORD *)a3,
                             a3);
  }
  else
  {
    if ( (int)a2 <= 1096250466 )
    {
      if ( (int)a2 > 1096249971 )
      {
        switch ( (int)a2 )
        {
          case 1096250211:
            *(_BYTE *)(a1 + 128) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            goto LABEL_122;
          case 1096250212:
          case 1096250213:
          case 1096250214:
          case 1096250215:
          case 1096250217:
          case 1096250218:
          case 1096250219:
          case 1096250220:
          case 1096250221:
          case 1096250223:
          case 1096250224:
          case 1096250225:
            return sub_140FE2700(a1, a2, a3);
          case 1096250216:
            if ( *(_BYTE *)(qword_141B600F0 + 89) == 0 )
            {
              sub_1407C9510(&v26);
              v20 = sub_14083D4F0();
              LODWORD(v29) = 0;
              v28 = (__int64 *)(v20 + 40);
              v3 = (__int64 *)&v28;
              sub_140835380(&v26, 1685353593, &v28);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v28 + 16))(v28, &v28);
              v21 = *(_DWORD *)(a1 + 12);
              v22 = sub_14083D4F0();
              LODWORD(v29) = v21;
              v28 = (__int64 *)(v22 + 40);
              sub_140835380(&v26, 1685417577, &v28);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v28 + 16))(v28, &v28);
              v23 = sub_14083D4F0();
              LODWORD(v29) = 1096250216;
              v28 = (__int64 *)(v23 + 56);
              sub_140835380(&v26, 1886549113, &v28);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v28 + 16))(v28, &v28);
              sub_1408351C0(&v26, 1853322860, a3);
              v24 = sub_140FE3DB0();
              v25 = sub_14083D4F0();
              LODWORD(v29) = v24;
              v28 = (__int64 *)(v25 + 40);
              sub_140835380(&v26, 1986359923, &v28);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v28 + 16))(v28, &v28);
              sub_140FFACE0(qword_141B600F0, &v26);
              sub_140833970(&v26);
              goto LABEL_122;
            }
            if ( (unsigned __int8)sub_1400870B0() != 0 )
            {
              sub_14141FB00(1095250288);
              sub_14141FB00(1095250544);
              sub_14141FB00(1095250800);
              sub_14141FB00(1095250292);
              sub_14141FB00(1095250548);
              sub_14141FB00(1095250804);
            }
            v26 = a1;
            sub_14151D370(v27, a1);
            v28 = &v26;
            v29 = v27;
            LODWORD(v3) = sub_140E4DEA0(&v28, a3);
            if ( (unsigned __int8)sub_1400870B0() != 0 )
              sub_14141FBC0();
            if ( v27[0] != 0 )
              sub_1407E4890(qword_141ABD470, v27[0], v27[2] - v27[0]);
            break;
          case 1096250222:
            v3 = &v26;
            (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 128LL))(
              *(_QWORD *)a3,
              &v26,
              a3);
            v9 = (volatile signed __int32 **)(a1 + 56);
            goto LABEL_92;
          case 1096250226:
            *(_BYTE *)(a1 + 132) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            goto LABEL_122;
          case 1096250227:
            *(_BYTE *)(a1 + 135) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            goto LABEL_122;
          default:
            if ( (_DWORD)a2 != 1096249972 )
              return sub_140FE2700(a1, a2, a3);
            *(_BYTE *)(a1 + 137) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            goto LABEL_122;
        }
        return (unsigned int)v3;
      }
      switch ( (_DWORD)a2 )
      {
        case 0x4157706F:
          *(_DWORD *)(a1 + 120) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 80LL))(
                                    *(_QWORD *)a3,
                                    a3);
          goto LABEL_122;
        case 0x41577262:
          *(_BYTE *)(a1 + 133) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
          goto LABEL_122;
        case 0x41577265:
          *(_WORD *)(a1 + 124) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
          goto LABEL_122;
        default:
          break;
      }
      return sub_140FE2700(a1, a2, a3);
    }
    if ( (int)a2 > 1096251239 )
    {
      if ( (int)a2 > 1096251488 )
      {
        if ( (_DWORD)a2 == 1096251489 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_BYTE *)(a1 + 143) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_BYTE *)(a1 + 143) = 0;
          goto LABEL_122;
        }
        if ( (_DWORD)a2 == 1145392197 )
        {
          *(_BYTE *)(a1 + 129) = -1;
          goto LABEL_122;
        }
      }
      else
      {
        if ( (_DWORD)a2 == 1096251240 )
        {
          *(_BYTE *)(a1 + 145) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 80LL))(
                                   *(_QWORD *)a3,
                                   a3);
          goto LABEL_122;
        }
        if ( (_DWORD)a2 == 1096251250 )
        {
          *(_BYTE *)(a1 + 146) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 80LL))(
                                   *(_QWORD *)a3,
                                   a3);
          goto LABEL_122;
        }
      }
      return sub_140FE2700(a1, a2, a3);
    }
    if ( (int)a2 > 1096250738 )
    {
      if ( (_DWORD)a2 == 1096250739 )
      {
        v10 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v11 = *(_BYTE *)(a1 + 141);
        if ( v10 != 0 )
          *(_BYTE *)(a1 + 141) = v11 | 1;
        else
          *(_BYTE *)(a1 + 141) = v11 & 0xFE;
        goto LABEL_122;
      }
      if ( (_DWORD)a2 == 1096250982 )
      {
        *(_BYTE *)(a1 + 138) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                 *(_QWORD *)a3,
                                 a3);
        goto LABEL_122;
      }
      return sub_140FE2700(a1, a2, a3);
    }
    if ( (_DWORD)a2 == 1096250467 )
    {
      sub_140FE3B40(&v26, a3);
      *(_DWORD *)(a1 + 32) = v26;
      goto LABEL_122;
    }
    if ( (_DWORD)a2 != 1096250489 )
      return sub_140FE2700(a1, a2, a3);
    *(_BYTE *)(a1 + 129) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                             *(_QWORD *)a3,
                             a3);
  }
LABEL_122:
  LOBYTE(v3) = 1;
  return (unsigned int)v3;
}
