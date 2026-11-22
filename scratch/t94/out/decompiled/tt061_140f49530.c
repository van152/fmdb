__int64 __fastcall sub_140F49530(__int64 a1, unsigned int a2)
{
  __int64 v2; // rsi
  char v3; // bl
  __int16 v4; // ax
  __int64 v5; // rax

  v2 = 0;
  v3 = a2;
  switch ( (int)a1 )
  {
    case 0:
      v2 = ((__int64 (*)(void))unk_140F71C00)();
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x14187B828LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_DWORD *)(v2 + 40) = 0;
      *(_BYTE *)(v2 + 44) = 1;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0x76C0001076C0001LL;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 96) = 0;
      *(_QWORD *)(v2 + 104) = 0;
      *(_QWORD *)(v2 + 112) = 0;
      *(_QWORD *)(v2 + 120) = 0;
      *(_QWORD *)(v2 + 128) = 0;
      *(_QWORD *)(v2 + 136) = 0;
      *(_DWORD *)(v2 + 144) = 0;
      *(_BYTE *)(v2 + 148) = -1;
      return v2;
    case 1:
      if ( byte_141B60320 == 0 )
        return 0;
      if ( byte_141B60461 != 0 )
      {
        v2 = ((__int64 (*)(void))unk_140F71CB0)();
        ((void (__fastcall *)(__int64))unk_140E4F7A0)(v2);
        *(_BYTE *)(v2 + 101) = v3;
        return v2;
      }
      if ( (_BYTE)a2 != 0 )
        return sub_1410992C0(a2);
      LOBYTE(a1) = 2;
      return sub_1410992C0(a1);
    case 2:
      v2 = ((__int64 (*)(void))unk_140F71D60)();
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x14187C7B8LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_WORD *)(v2 + 80) = 0;
      *(_DWORD *)(v2 + 82) = 1;
      return v2;
    case 3:
      if ( (_BYTE)a2 == 12 )
      {
        v2 = ((__int64 (*)(void))unk_140F71E10)();
        ((void (__fastcall *)(__int64))unk_140E5A440)(v2);
        *(_QWORD *)v2 = 0x1418BFBF8LL;
        *(_QWORD *)(v2 + 368) = 0;
        *(_BYTE *)(v2 + 376) = 0;
      }
      else
      {
        v2 = ((__int64 (*)(void))unk_140F71EC0)();
        ((void (__fastcall *)(__int64))unk_140E5A440)(v2);
      }
      return v2;
    case 4:
      v2 = ((__int64 (*)(void))unk_140F71F70)();
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141882578LL;
      return v2;
    case 5:
      v2 = sub_141750CC0(248);
      ((void (__fastcall *)(__int64))unk_140ED6480)(v2);
      return v2;
    case 6:
      v2 = ((__int64 (*)(void))unk_140F720D0)();
      *(_QWORD *)v2 = 0;
      *(_QWORD *)(v2 + 8) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      ((void (__fastcall *)(__int64))unk_140F72180)(v2);
      return v2;
    case 7:
      v2 = ((__int64 (*)(void))unk_140F72200)();
      ((void (__fastcall *)(__int64))unk_141546080)(v2);
      return v2;
    case 8:
      v2 = ((__int64 (*)(void))unk_140F722B0)();
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x141888DB8LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_DWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 52) = 0x100010001LL;
      *(_BYTE *)(v2 + 60) = 0;
      return v2;
    case 9:
      v2 = ((__int64 (*)(void))unk_140F72360)();
      sub_14105A430(v2);
      return v2;
    case 10:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72020)(472);
      sub_14103F5F0(v2);
      return v2;
    case 12:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72410)(160);
      ((void (__fastcall *)(__int64, _QWORD))unk_14118DC00)(v2, 0);
      return v2;
    case 14:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F6B6D0)(88);
      ((void (__fastcall *)(__int64))unk_140F6B780)(v2);
      return v2;
    case 18:
      v2 = ((__int64 (*)(void))unk_140F74080)();
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x141887278LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 96) = -4170448895LL;
      *(_QWORD *)(v2 + 104) = 0;
      *(_WORD *)(v2 + 118) = -1;
      *(_DWORD *)(v2 + 120) = 0;
      *(_WORD *)(v2 + 124) = 0;
      *(_DWORD *)(v2 + 112) = -1;
      *(_WORD *)(v2 + 116) = -1;
      return v2;
    case 19:
      v2 = ((__int64 (*)(void))unk_140F724C0)();
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x1418BF628LL;
      *(_WORD *)(v2 + 72) = 1024;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = -1;
      *(_QWORD *)(v2 + 48) = 0xFFFFFFFFLL;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = -1;
      return v2;
    case 21:
      v2 = ((__int64 (*)(void))unk_140F72570)();
      ((void (__fastcall *)(__int64, __int64))unk_141184670)(v2, 0xFFFFFFFFLL);
      return v2;
    case 22:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140E98490)(112);
      ((void (__fastcall *)(__int64))unk_141538170)(v2);
      return v2;
    case 23:
      v2 = ((__int64 (*)(void))unk_140F72620)();
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x1418828F8LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_DWORD *)(v2 + 56) = 0;
      return v2;
    case 24:
      if ( byte_141B60320 != 0 )
      {
        if ( (_BYTE)a2 == 11 )
        {
          v2 = ((__int64 (__fastcall *)(__int64))unk_140F72780)(256);
          ((void (__fastcall *)(__int64))unk_141053530)(v2);
        }
        else
        {
          v2 = ((__int64 (__fastcall *)(__int64))unk_140F72830)(184);
          ((void (__fastcall *)(__int64))unk_1411A0B60)(v2);
        }
      }
      else
      {
        v2 = ((__int64 (*)(void))unk_140F6F350)();
        *(_QWORD *)(v2 + 16) = 0;
        *(_QWORD *)(v2 + 8) = -1;
        *(_QWORD *)v2 = 0x141882C78LL;
        *(_QWORD *)(v2 + 40) = 0xFFFF00000000LL;
        *(_QWORD *)(v2 + 24) = 0;
        *(_QWORD *)(v2 + 32) = 0;
        *(_QWORD *)(v2 + 48) = 0;
      }
      return v2;
    case 25:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F6EAE0)(432);
      sub_140EB67B0(v2);
      return v2;
    case 26:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F728E0)(120);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x1418BE248LL;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 96) = 0;
      *(_QWORD *)(v2 + 104) = 0x7D0076C0001LL;
      *(_DWORD *)(v2 + 112) = 131074000;
      *(_WORD *)(v2 + 116) = 0;
      *(_BYTE *)(v2 + 118) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      return v2;
    case 27:
      v2 = ((__int64 (*)(void))unk_140F72990)();
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 96) = 0;
      *(_QWORD *)(v2 + 104) = 0;
      *(_QWORD *)(v2 + 112) = 0;
      *(_QWORD *)(v2 + 120) = 0;
      *(_QWORD *)(v2 + 128) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141882DE8LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 46) = 0;
      *(_BYTE *)(v2 + 54) = 100;
      *(_QWORD *)(v2 + 70) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_BYTE *)(v2 + 78) = 100;
      *(_QWORD *)(v2 + 94) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 80) = 0;
      *(_BYTE *)(v2 + 102) = 100;
      *(_QWORD *)(v2 + 118) = 0;
      *(_QWORD *)(v2 + 104) = 0;
      *(_QWORD *)(v2 + 112) = 0;
      *(_BYTE *)(v2 + 126) = 100;
      *(_BYTE *)(v2 + 129) = 0;
      return v2;
    case 29:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72AF0)(104);
      *(_QWORD *)v2 = 0;
      *(_QWORD *)(v2 + 8) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 96) = 0;
      ((void (__fastcall *)(__int64))unk_140F72BA0)(v2);
      return v2;
    case 30:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72C20)(56);
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141883268LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0x76C0001076C0001LL;
      *(_BYTE *)(v2 + 51) = 3;
      return v2;
    case 31:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72CD0)(40);
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141883428LL;
      return v2;
    case 32:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73400)(136);
      ((void (__fastcall *)(__int64, _QWORD, __int64))unk_141758A10)(v2, 0, 136);
      sub_140F734B0(v2);
      return v2;
    case 33:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72D80)(104);
      *(_QWORD *)v2 = 0;
      *(_QWORD *)(v2 + 8) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 96) = 0;
      ((void (__fastcall *)(__int64))unk_140F72E30)(v2);
      return v2;
    case 34:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72F70)(80);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x1418BE628LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_DWORD *)(v2 + 72) = 124520300;
      *(_WORD *)(v2 + 76) = 0;
      *(_BYTE *)(v2 + 78) = -1;
      return v2;
    case 35:
      v2 = ((__int64 (*)(void))unk_140F73FD0)();
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141885128LL;
      *(_BYTE *)(v2 + 32) = 0;
      return v2;
    case 36:
      v2 = ((__int64 (*)(void))unk_140F72EC0)();
      ((void (__fastcall *)(__int64))unk_14157E1E0)(v2);
      return v2;
    case 37:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140042440)(64);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x14188E118LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 54) = 0;
      *(_BYTE *)(v2 + 62) = 24;
      return v2;
    case 38:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140DD0A30)(56);
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141877848LL;
      *(_QWORD *)(v2 + 32) = 0x76C0001076C0001LL;
      *(_QWORD *)(v2 + 40) = -1;
      *(_DWORD *)(v2 + 48) = -1;
      return v2;
    case 39:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73020)(88);
      sub_140F730D0(v2);
      return v2;
    case 41:
      v2 = ((__int64 (*)(void))unk_140F74130)();
      ((void (__fastcall *)(__int64))unk_14157F380)(v2);
      return v2;
    case 42:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F731F0)(40);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x141883908LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_DWORD *)(v2 + 32) = 124518401;
      *(_BYTE *)(v2 + 36) = 1;
      return v2;
    case 43:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F732A0)(64);
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141883A68LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_QWORD *)(v2 + 32) = -1;
      *(_QWORD *)(v2 + 40) = -1;
      *(_BYTE *)(v2 + 56) = 1;
      return v2;
    case 44:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F6BA00)(64);
      ((void (__fastcall *)(__int64))unk_141454310)(v2);
      return v2;
    case 45:
    case 48:
      if ( dword_141B5E1F8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        ((void (__fastcall *)(int *))unk_141750E08)(&dword_141B5E1F8);
        if ( dword_141B5E1F8 == -1 )
        {
          ((void (__fastcall *)(void *, __int64, __int64, __int64, _BYTE, char, int, __int64))unk_1407E53D0)(
            &unk_141B5E1A8,
            0x141930B55LL,
            10000,
            96,
            0,
            1,
            10000,
            4096);
          ((void (__fastcall *)(void *))unk_141751048)(&unk_140ED17F0);
          ((void (__fastcall *)(int *))unk_141750EA0)(&dword_141B5E1F8);
        }
      }
      v2 = ((__int64 (__fastcall *)(void *, __int64))unk_1407E58C0)(&unk_141B5E1A8, 96);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x14187DF38LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_QWORD *)(v2 + 32) = -1;
      *(_QWORD *)(v2 + 40) = -1;
      *(_QWORD *)(v2 + 48) = -1;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 64) = 0x76C0001076C0001LL;
      *(_DWORD *)(v2 + 72) = 124518401;
      *(_QWORD *)(v2 + 76) = -1;
      *(_QWORD *)(v2 + 84) = -1;
      *(_BYTE *)(v2 + 92) = -1;
      *(_WORD *)(v2 + 93) = 0;
      return v2;
    case 46:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73630)(40);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x141883E88LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_WORD *)(v2 + 32) = -1;
      v4 = word_141AB0260;
      if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
      {
        word_141AB0260 = 2023;
        v4 = 2023;
      }
      *(_WORD *)(v2 + 34) = v4;
      return v2;
    case 47:
      v2 = ((__int64 (*)(void))unk_140F741E0)();
      ((void (__fastcall *)(__int64))unk_141458F90)(v2);
      return v2;
    case 49:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F736E0)(48);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x1418B6C88LL;
      *(_QWORD *)(v2 + 32) = 0x76C0001FFFFFFFFLL;
      *(_DWORD *)(v2 + 40) = -1;
      *(_BYTE *)(v2 + 46) = 0;
      *(_QWORD *)(v2 + 24) = -1;
      *(_WORD *)(v2 + 44) = 1;
      return v2;
    case 50:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73790)(40);
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141883FE8LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_DWORD *)(v2 + 32) = 124518401;
      *(_BYTE *)(v2 + 36) = -1;
      return v2;
    case 51:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73840)(40);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      v5 = 0x141884148LL;
      goto LABEL_62;
    case 52:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73BB0)(48);
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141884828LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_DWORD *)(v2 + 40) = -1;
      return v2;
    case 56:
      v2 = ((__int64 (*)(void))unk_140F726D0)();
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141882AB8LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_WORD *)(v2 + 48) = 0;
      return v2;
    case 57:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F74290)(72);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x1418852E8LL;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_BYTE *)(v2 + 56) = 0;
      return v2;
    case 58:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73350)(56);
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141883BC8LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_QWORD *)(v2 + 32) = -1;
      *(_QWORD *)(v2 + 40) = -1;
      *(_QWORD *)(v2 + 48) = 124518401;
      return v2;
    case 59:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F72A40)(64);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x141882FA8LL;
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = ((__int64 (*)(void))unk_1407E4940)();
      *(_BYTE *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      return v2;
    case 60:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F738F0)(40);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      v5 = 0x1418842A8LL;
LABEL_62:
      *(_QWORD *)v2 = v5;
      *(_QWORD *)(v2 + 24) = 0xFFFFFFFFLL;
      *(_WORD *)(v2 + 32) = 1900;
      return v2;
    case 61:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F739A0)(32);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x141884408LL;
      *(_DWORD *)(v2 + 24) = -1;
      *(_BYTE *)(v2 + 28) = 0;
      *(_WORD *)(v2 + 30) = 1900;
      return v2;
    case 62:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73C60)(80);
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141884988LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_DWORD *)(v2 + 64) = 0;
      *(_BYTE *)(v2 + 68) = -1;
      *(_BYTE *)(v2 + 72) = -1;
      return v2;
    case 63:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73A50)(32);
      *(_QWORD *)(v2 + 8) = -1;
      *(_DWORD *)(v2 + 16) = 0;
      *(_QWORD *)v2 = 0x141884568LL;
      *(_DWORD *)(v2 + 24) = -1;
      *(_BYTE *)(v2 + 28) = -1;
      *(_WORD *)(v2 + 30) = 1900;
      return v2;
    case 64:
      v2 = ((__int64 (*)(void))unk_140F73D10)();
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141884B48LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_DWORD *)(v2 + 32) = 0;
      return v2;
    case 65:
    case 67:
    case 68:
    case 69:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73DC0)(48);
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)(v2 + 24) = 0xFFFFFFF9FFFFFFF9uLL;
      *(_QWORD *)v2 = 0x141884CA8LL;
      *(_DWORD *)(v2 + 40) = -1;
      return v2;
    case 66:
      v2 = sub_141750CC0(40);
      *(_OWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141884E08LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_WORD *)(v2 + 33) = 11534;
      return v2;
    case 70:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73E70)(64);
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x141884F68LL;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 40) = -1;
      *(_DWORD *)(v2 + 50) = 124520300;
      *(_DWORD *)(v2 + 54) = 0;
      *(_BYTE *)(v2 + 58) = 0;
      return v2;
    case 71:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73F20)(96);
      ((void (__fastcall *)(__int64, _QWORD))unk_1411990C0)(v2, 0);
      return v2;
    case 72:
      v2 = sub_141750CC0(240);
      ((void (__fastcall *)(__int64))unk_14153E950)(v2);
      return v2;
    case 73:
      v2 = ((__int64 (__fastcall *)(__int64))unk_140F73B00)(40);
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 16) = 0;
      *(_QWORD *)(v2 + 8) = -1;
      *(_QWORD *)v2 = 0x1418846C8LL;
      *(_QWORD *)(v2 + 24) = -1;
      *(_WORD *)(v2 + 32) = 1900;
      return v2;
    default:
      return v2;
  }
}
