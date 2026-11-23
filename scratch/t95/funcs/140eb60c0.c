char __fastcall sub_140EB60C0(__int64 *a1, int a2, __int64 *a3)
{
  char result; // al
  __int64 v6; // rcx
  int v7; // eax
  char v8; // di
  __int64 v9; // rax
  __int64 *v10; // rax
  __int64 v11; // rcx
  __int64 *v12; // rcx
  __int64 *v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rcx
  int v16; // eax
  int v17; // ecx
  char v18; // bl
  __int64 *v19; // rax
  __int64 v20; // rcx
  char v21; // bl
  __int64 *v22; // rax
  __int64 v23; // rcx
  __int64 *v24; // [rsp+20h] [rbp-10h] BYREF
  __int64 v25; // [rsp+28h] [rbp-8h]
  __int64 v26; // [rsp+30h] [rbp+0h]

  v26 = -2;
  result = 0;
  v6 = (unsigned int)(a2 - 1212892516);
  switch ( a2 )
  {
    case 1212892516:
LABEL_9:
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
      LODWORD(v25) = ((a1[2] & 0x1FF) << 8)
                   | (*((unsigned __int16 *)a1 + 8) >> 9)
                   | (*((unsigned __int16 *)a1 + 9) << 17);
      v12 = &qword_141B5C8A0;
      v24 = &qword_141B5C8A0;
      if ( &v24 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v13 = v24;
        v14 = v25;
        a3[1] = v25;
        *a3 = (__int64)v13;
        v12 = (__int64 *)(sub_14083D4F0(v14) + 8);
        v25 = 0;
        v24 = v12;
      }
      (*(void (__fastcall **)(__int64 *, __int64 **))(*v12 + 16))(v12, &v24);
      goto LABEL_26;
    case 1212892517:
    case 1212892518:
    case 1212892519:
    case 1212892520:
    case 1212892521:
    case 1212892522:
    case 1212892523:
    case 1212892524:
    case 1212892526:
    case 1212892527:
    case 1212892528:
    case 1212892529:
    case 1212892530:
    case 1212892533:
      return result;
    case 1212892525:
LABEL_13:
      v15 = *a1;
      if ( *a1 != 0 )
        goto LABEL_14;
      goto LABEL_18;
    case 1212892531:
LABEL_17:
      v15 = a1[1];
      if ( v15 != 0 )
      {
LABEL_14:
        v16 = *(_DWORD *)(v15 + 12);
        v17 = *(_DWORD *)(v15 + 16);
        if ( v17 == 0 )
          v17 = v16;
      }
      else
      {
LABEL_18:
        v16 = -1;
        v17 = -1;
      }
      v24 = (__int64 *)__PAIR64__(v17, v16);
      sub_140FE72B0((int *)&v24, 1937008494, a3);
      goto LABEL_26;
    case 1212892532:
      v21 = *((_BYTE *)a1 + 20);
      v9 = sub_14083D4F0(v6) + 24;
      LOBYTE(v25) = v21 == 100;
      v24 = (__int64 *)v9;
      if ( &v24 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v22 = v24;
        v23 = v25;
        a3[1] = v25;
        *a3 = (__int64)v22;
        v9 = sub_14083D4F0(v23) + 8;
        v25 = 0;
        v24 = (__int64 *)v9;
      }
      goto LABEL_25;
    case 1212892534:
LABEL_20:
      v18 = *((_BYTE *)a1 + 21);
      v9 = sub_14083D4F0(v6) + 24;
      LOBYTE(v25) = v18;
      v24 = (__int64 *)v9;
      if ( &v24 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v19 = v24;
        v20 = v25;
        a3[1] = v25;
        *a3 = (__int64)v19;
        v9 = sub_14083D4F0(v20) + 8;
        v25 = 0;
        v24 = (__int64 *)v9;
      }
LABEL_25:
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v9 + 16LL))(v9, &v24);
LABEL_26:
      result = 1;
      break;
    default:
      switch ( a2 )
      {
        case 1447121508:
          goto LABEL_9;
        case 1447121517:
          goto LABEL_13;
        case 1447121523:
          goto LABEL_17;
        case 1447121524:
          v7 = *((_DWORD *)a1 + 5);
          v8 = 4;
          if ( (_BYTE)v7 != 0 )
            v8 = v7;
          v9 = sub_14083D4F0(v6) + 40;
          LODWORD(v25) = v8;
          v24 = (__int64 *)v9;
          if ( &v24 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v10 = v24;
            v11 = v25;
            a3[1] = v25;
            *a3 = (__int64)v10;
            v9 = sub_14083D4F0(v11) + 8;
            v25 = 0;
            v24 = (__int64 *)v9;
          }
          goto LABEL_25;
        case 1447121526:
          goto LABEL_20;
        default:
          return result;
      }
  }
  return result;
}
